from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, products

app = FastAPI(
    title="汇农亩场 API",
    description="农产品交易平台后端服务",
    version="0.1.0",
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


@app.get("/")
async def root():
    return {"message": "欢迎使用汇农亩场 API，请访问 /docs 查看接口文档"}
