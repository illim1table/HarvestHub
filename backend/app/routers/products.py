import math
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.routers.auth import require_roles
from app.schemas.common import APIResponse, PaginationMeta
from app.schemas.product import ProductCreate, ProductListData, ProductRead, ProductUpdate

router = APIRouter()


def to_product_read(product: Product, seller_name: str, category_name: str) -> ProductRead:
    return ProductRead(
        id=product.id,
        name=product.name,
        description=product.description,
        price=float(product.price),
        unit=product.unit,
        stock=product.stock,
        image_url=product.image_url,
        seller_id=product.seller_id,
        category_id=product.category_id,
        created_at=product.created_at,
        seller_name=seller_name,
        category_name=category_name,
    )


async def get_product_row(db: AsyncSession, product_id: int):
    stmt = (
        select(Product, Category.name, User.username)
        .join(Category, Product.category_id == Category.id)
        .join(User, Product.seller_id == User.id)
        .where(Product.id == product_id)
    )
    return (await db.execute(stmt)).first()


def ensure_product_permission(current_user: User, product: Product) -> None:
    user_role = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if user_role == "admin":
        return
    if user_role != "seller" or product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限操作该商品")


@router.post(
    "/products",
    response_model=APIResponse[ProductRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller", "admin")),
):
    category = await db.get(Category, payload.category_id)
    if not category or not category.is_active:
        raise HTTPException(status_code=404, detail="分类不存在或已停用")

    product = Product(
        name=payload.name,
        description=payload.description,
        price=Decimal(str(payload.price)),
        unit=payload.unit,
        stock=payload.stock,
        image_url=payload.image_url,
        seller_id=current_user.id,
        category_id=payload.category_id,
    )
    db.add(product)
    await db.commit()

    row = await get_product_row(db, product.id)
    if not row:
        raise HTTPException(status_code=500, detail="商品创建成功但查询失败")

    product_obj, category_name, seller_name = row
    return APIResponse(data=to_product_read(product_obj, seller_name, category_name))


@router.get("/products", response_model=APIResponse[ProductListData])
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    filters = [Category.is_active.is_(True)]
    if category_id is not None:
        filters.append(Product.category_id == category_id)

    count_stmt = select(func.count(Product.id)).join(Category, Product.category_id == Category.id).where(*filters)
    total = int((await db.scalar(count_stmt)) or 0)

    stmt = (
        select(Product, Category.name, User.username)
        .join(Category, Product.category_id == Category.id)
        .join(User, Product.seller_id == User.id)
        .where(*filters)
        .order_by(Product.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    rows = (await db.execute(stmt)).all()
    items = [to_product_read(product, seller_name, category_name) for product, category_name, seller_name in rows]

    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return APIResponse(
        data=ProductListData(
            items=items,
            pagination=PaginationMeta(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
            ),
        )
    )


@router.get("/products/{product_id}", response_model=APIResponse[ProductRead])
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    row = await get_product_row(db, product_id)
    if not row:
        raise HTTPException(status_code=404, detail="商品不存在")

    product, category_name, seller_name = row
    return APIResponse(data=to_product_read(product, seller_name, category_name))


@router.put("/products/{product_id}", response_model=APIResponse[ProductRead])
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller", "admin")),
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    ensure_product_permission(current_user, product)

    update_data = payload.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        category = await db.get(Category, update_data["category_id"])
        if not category or not category.is_active:
            raise HTTPException(status_code=404, detail="分类不存在或已停用")

    if "price" in update_data and update_data["price"] is not None:
        update_data["price"] = Decimal(str(update_data["price"]))

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()

    row = await get_product_row(db, product_id)
    if not row:
        raise HTTPException(status_code=404, detail="商品不存在")
    product_obj, category_name, seller_name = row
    return APIResponse(data=to_product_read(product_obj, seller_name, category_name))


@router.delete("/products/{product_id}", response_model=APIResponse[dict[str, int]])
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller", "admin")),
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    ensure_product_permission(current_user, product)

    await db.delete(product)
    await db.commit()
    return APIResponse(data={"deleted_id": product_id})
