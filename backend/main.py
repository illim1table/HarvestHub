from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import auth, categories, health, orders, payments, products


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="汇农亩场 API",
    description="农产品交易平台后端服务",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    # TODO: Restrict to specific origins in production (e.g. ["https://yourdomain.com"])
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["健康检查"])
app.include_router(products.router, prefix="/api", tags=["商品"])
app.include_router(categories.router, prefix="/api", tags=["分类"])
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(orders.router, prefix="/api", tags=["订单"])
app.include_router(orders.seller_router, prefix="/api", tags=["卖家订单"])
app.include_router(payments.router, prefix="/api", tags=["支付"])


@app.get("/")
async def root():
    return {"message": "欢迎使用汇农亩场 API，请访问 /docs 查看接口文档"}
