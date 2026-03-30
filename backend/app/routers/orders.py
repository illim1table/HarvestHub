from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
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
from app.schemas.order import OrderCreate, OrderItemRead, OrderListData, OrderRead

router = APIRouter()


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


def to_order_read(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        buyer_id=order.buyer_id,
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=[to_order_item_read(item) for item in order.items],
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
        if product.stock <= 0:
            raise HTTPException(status_code=400, detail=f"商品不可售（库存为0）: {product.name}")
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("consumer", "admin")),
):
    stmt = (
        select(Order)
        .where(Order.buyer_id == current_user.id)
        .order_by(Order.created_at.desc())
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
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
    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="仅支持取消待支付订单")

    for item in order.items:
        if item.product:
            item.product.stock += item.quantity
    order.status = OrderStatus.cancelled
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
