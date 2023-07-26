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
