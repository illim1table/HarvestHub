from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.schemas.common import APIResponse
from app.schemas.order import MockPaymentRequest, OrderRead, PayStatus
from app.routers.orders import ensure_order_transition, to_order_read

router = APIRouter(prefix="/payments")


@router.post("/mock", response_model=APIResponse[OrderRead])
async def mock_payment_callback(payload: MockPaymentRequest, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Order)
        .where(Order.id == payload.order_id)
        .with_for_update()
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if payload.pay_status == PayStatus.failed:
        if order.status != OrderStatus.pending:
            raise HTTPException(status_code=400, detail="当前订单状态不支持支付失败回调")
        return APIResponse(data=to_order_read(order), message="已接收支付失败回调")

    if order.status == OrderStatus.paid:
        if order.payment_trade_no and order.payment_trade_no != payload.trade_no:
            raise HTTPException(status_code=400, detail="订单已支付，交易号不一致")
        return APIResponse(data=to_order_read(order), message="重复支付回调，已幂等处理")

    ensure_order_transition(order, OrderStatus.paid)
    order.status = OrderStatus.paid
    order.payment_trade_no = payload.trade_no
    if order.paid_at is None:
        order.paid_at = datetime.utcnow()
    await db.commit()

    refreshed_stmt = (
        select(Order)
        .where(Order.id == payload.order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    refreshed_order = await db.scalar(refreshed_stmt)
    if not refreshed_order:
        raise HTTPException(status_code=500, detail="支付回调处理成功但订单查询失败")

    return APIResponse(data=to_order_read(refreshed_order), message="支付成功")
