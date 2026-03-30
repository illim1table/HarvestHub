from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.routers.auth import require_roles
from app.schemas.category import CategoryCreate, CategoryRead
from app.schemas.common import APIResponse

router = APIRouter()


@router.get("/categories", response_model=APIResponse[list[CategoryRead]])
async def get_categories(db: AsyncSession = Depends(get_db)):
    stmt = select(Category).where(Category.is_active.is_(True)).order_by(Category.created_at.desc())
    categories = (await db.scalars(stmt)).all()
    return APIResponse(data=[CategoryRead.model_validate(item) for item in categories])


@router.post(
    "/categories",
    response_model=APIResponse[CategoryRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("seller", "admin")),
):
    existing_stmt = select(Category).where(Category.name == payload.name)
    existing = await db.scalar(existing_stmt)
    if existing:
        raise HTTPException(status_code=400, detail="分类名称已存在")

    category = Category(
        name=payload.name,
        description=payload.description,
        is_active=payload.is_active,
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return APIResponse(data=CategoryRead.model_validate(category))
