from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dependencies import get_db_session
from src.database.repositories import UserRepository
from src.schemas.users import UserCreate, UserUpdate, UserRead


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db_session)):
    return await UserRepository.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    return await UserRepository.create(db, data)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return await UserRepository.update(db, user, data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    await UserRepository.delete(db, user)
    return None
