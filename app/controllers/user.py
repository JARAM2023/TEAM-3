from http.client import HTTPException
from typing import Dict

from django.http import JsonResponse
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from rest_framework import status
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


class user_change(BaseModel):
    height: float
    weight: float
    gender: int

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


@router.patch("/{user_id}")
def update_user(user_id: int, item: user_change, session: Session = Depends(get_session)) -> dict[str, str]:
    user: m.User | None = session.execute(sql_exp.select(m.User).where(m.User.id == user_id)).scalar_one_or_none()

    if item.height is not None:
        user.height = item.height
    if item.weight is not None:
        user.weight = item.weight
    if item.gender is not None:
        user.gender = item.gender
    return {"message": "User data updated sucesssfully"}

'''
    stored_item_data = m.User[user_id]
    stored_item_model = user_change(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    m.User[user_id] = jsonable_encoder(updated_item)
    return updated_item
    '''
