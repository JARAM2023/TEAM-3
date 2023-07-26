from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql_exp

from app import models as m
from app.utils.rdb import get_session

router = APIRouter(prefix="/user", tags=["user"])


class User(BaseModel):
    id: int
    username: str
    height: float
    weight: float
    gender: int
    class Config:
        orm_mode = True

class Diet(BaseModel):
    food_id: int

    class Config:
        orm_mode = True



@router.get("/{user_id}")
def user_get(
    user_id: int,
    session: Session = Depends(get_session)
) -> User:
    user: m.User | None = session.execute(
        sql_exp
        .select(m.User)
        .where(m.User.id == user_id)
    ).scalar_one_or_none()

    return User.from_orm(user)

@router.get("/{user_id}/diet/list")
def diet_get(
        user_id: int,
        session: Session = Depends(get_session)
) -> Diet:
    diet: m.Diet | None = session.execute(
        sql_exp
        .select(m.Diet)
        .where(m.Diet.diet_user_id == user_id)
    ).scalar_one_or_none()

    return Diet.from_orm(diet)

@router.post("/{user_id}/diet")
def diet_post(user_id: int, item: Diet):
    return JsonResponse(item, status=status.HTTP_201_CREATED)

