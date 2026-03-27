from fastapi import APIRouter, HTTPException
from typing import List
from app.models.product import Product

router = APIRouter()

MOCK_PRODUCTS: List[Product] = [
    Product(
        id=1,
        name="有机红富士苹果",
        category="水果",
        price=12.80,
        unit="斤",
        stock=500,
        description="产自山东烟台，有机种植，果肉鲜脆，甜而不腻",
        seller="烟台果园直营店",
        image_url="https://placehold.co/300x200?text=苹果",
    ),
    Product(
        id=2,
        name="新鲜大白菜",
        category="蔬菜",
        price=1.50,
        unit="斤",
        stock=1000,
        description="当日现摘，叶绿水灵，适合炒菜、做汤",
        seller="京郊有机农场",
        image_url="https://placehold.co/300x200?text=白菜",
    ),
    Product(
        id=3,
        name="土鸡蛋",
        category="禽蛋",
        price=18.00,
        unit="30枚/盒",
        stock=200,
        description="散养土鸡，每日新鲜采集，蛋黄金黄营养丰富",
        seller="农家散养鸡场",
        image_url="https://placehold.co/300x200?text=鸡蛋",
    ),
    Product(
        id=4,
        name="东北五常大米",
        category="粮食",
        price=45.00,
        unit="5kg/袋",
        stock=300,
        description="五常稻花香2号，米粒饱满，蒸出来香气四溢",
        seller="五常稻田直供",
        image_url="https://placehold.co/300x200?text=大米",
    ),
    Product(
        id=5,
        name="云南野生蜂蜜",
        category="农副产品",
        price=88.00,
        unit="500g/瓶",
        stock=80,
        description="云南深山野生蜂巢采集，纯天然无添加",
        seller="云南山货铺",
        image_url="https://placehold.co/300x200?text=蜂蜜",
    ),
    Product(
        id=6,
        name="新鲜草莓",
        category="水果",
        price=25.00,
        unit="500g/盒",
        stock=150,
        description="丹东99草莓，颗粒饱满，酸甜可口",
        seller="丹东草莓园",
        image_url="https://placehold.co/300x200?text=草莓",
    ),
]


@router.get("/products", response_model=List[Product])
async def get_products():
    return MOCK_PRODUCTS


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in MOCK_PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="商品不存在")
