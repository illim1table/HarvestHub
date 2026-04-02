from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.routers.auth import require_roles
from app.schemas.common import APIResponse
from app.schemas.order import OrderCreate, OrderItemRead, OrderListData, OrderRead, SellerOrderListData

router = APIRouter()
seller_router = APIRouter(prefix="/seller")


ALLOWED_ORDER_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.pending: {OrderStatus.paid, OrderStatus.cancelled},
    OrderStatus.paid: {OrderStatus.completed},
    OrderStatus.cancelled: set(),
    OrderStatus.completed: set(),
}


def ensure_order_transition(order: Order, target_status: OrderStatus) -> None:
    allowed_targets = ALLOWED_ORDER_TRANSITIONS.get(order.status, set())
    if target_status not in allowed_targets:
        raise HTTPException(
            status_code=400,
            detail=f"非法状态流转: {order.status.value} -> {target_status.value}",
        )


def to_order_item_read(item: OrderItem) -> OrderItemRead:
    product_name = item.product.name if item.product else ""
    return OrderItemRead(
        id=item.id,
        product_id=item.product_id,
        product_name=product_name,
        price=float(item.price),
        quantity=item.quantity,
        amount=float(item.amount),
    )


def to_order_read(order: Order, seller_id: int | None = None) -> OrderRead:
    items = order.items
    total_amount = order.total_amount
    if seller_id is not None:
        items = [item for item in order.items if item.product and item.product.seller_id == seller_id]
        total_amount = sum((item.amount for item in items), Decimal('0.00'))

    return OrderRead(
        id=order.id,
        buyer_id=order.buyer_id,
        status=order.status,
        total_amount=float(total_amount),
        payment_trade_no=order.payment_trade_no,
        paid_at=order.paid_at,
        completed_at=order.completed_at,
        cancelled_at=order.cancelled_at,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=[to_order_item_read(item) for item in items],
    )


@router.post("/orders", response_model=APIResponse[OrderRead], status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    quantities: dict[int, int] = {}
    for item in payload.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity

    product_ids = list(quantities.keys())
    products_stmt = select(Product).where(Product.id.in_(product_ids)).with_for_update()
    products = (await db.scalars(products_stmt)).all()
    product_map = {product.id: product for product in products}

    missing_ids = [product_id for product_id in product_ids if product_id not in product_map]
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"商品不存在: {missing_ids}")

    order_items: list[OrderItem] = []
    total_amount = Decimal("0.00")

    for product_id, quantity in quantities.items():
        product = product_map[product_id]
        if product.stock < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"库存不足: {product.name}（剩余 {product.stock}，需求 {quantity}）",
            )

        price = Decimal(str(product.price))
        amount = price * quantity
        total_amount += amount
        product.stock -= quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                price=price,
                quantity=quantity,
                amount=amount,
            )
        )

    order = Order(
        buyer_id=current_user.id,
        status=OrderStatus.pending,
        total_amount=total_amount,
        items=order_items,
    )
    db.add(order)
    await db.commit()

    detail_stmt = (
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    created_order = await db.scalar(detail_stmt)
    if not created_order:
        raise HTTPException(status_code=500, detail="订单创建成功但查询失败")
    return APIResponse(data=to_order_read(created_order))


@router.get("/orders", response_model=APIResponse[OrderListData])
async def get_my_orders(
    status_filter: OrderStatus | None = Query(default=None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.buyer_id == current_user.id)
        .order_by(Order.created_at.desc())
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    if status_filter is not None:
        stmt = stmt.where(Order.status == status_filter)

    orders = (await db.scalars(stmt)).all()
    return APIResponse(data=OrderListData(items=[to_order_read(order) for order in orders]))


@router.get("/orders/{order_id}", response_model=APIResponse[OrderRead])
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限查看该订单")
    return APIResponse(data=to_order_read(order))


@router.put("/orders/{order_id}/cancel", response_model=APIResponse[OrderRead])
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .with_for_update()
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限取消该订单")

    ensure_order_transition(order, OrderStatus.cancelled)

    for item in order.items:
        if item.product:
            item.product.stock += item.quantity

    order.status = OrderStatus.cancelled
    order.cancelled_at = datetime.now()
    await db.commit()

    refreshed_stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    refreshed_order = await db.scalar(refreshed_stmt)
    if not refreshed_order:
        raise HTTPException(status_code=500, detail="订单取消成功但查询失败")
    return APIResponse(data=to_order_read(refreshed_order))


@router.put("/orders/{order_id}/confirm", response_model=APIResponse[OrderRead])
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .with_for_update()
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限确认收货")

    ensure_order_transition(order, OrderStatus.completed)
    order.status = OrderStatus.completed
    order.completed_at = datetime.now()
    await db.commit()

    refreshed_stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    refreshed_order = await db.scalar(refreshed_stmt)
    if not refreshed_order:
        raise HTTPException(status_code=500, detail="确认收货成功但查询失败")
    return APIResponse(data=to_order_read(refreshed_order))


@seller_router.get("/orders", response_model=APIResponse[SellerOrderListData])
async def get_seller_orders(
    status_filter: OrderStatus | None = Query(default=None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller", "admin")),
):
    stmt = (
        select(Order)
        .join(Order.items)
        .join(OrderItem.product)
        .where(Product.seller_id == current_user.id)
        .order_by(Order.created_at.desc())
        .distinct()
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    if status_filter is not None:
        stmt = stmt.where(Order.status == status_filter)

    orders = (await db.scalars(stmt)).all()
    data = [to_order_read(order, seller_id=current_user.id) for order in orders]
    return APIResponse(data=SellerOrderListData(items=data))


@seller_router.get("/orders/{order_id}", response_model=APIResponse[OrderRead])
async def get_seller_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    has_permission = any(
        item.product and item.product.seller_id == current_user.id for item in order.items
    )
    if not has_permission:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限查看该卖家订单")

    return APIResponse(data=to_order_read(order, seller_id=current_user.id))
