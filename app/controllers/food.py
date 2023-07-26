from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql_exp

from app import models as m
from app.utils.rdb import get_session

router = APIRouter(prefix="/food", tags=["food"])


class Food(BaseModel):
    id: int
    name: str
    carbo: float
    protein: float
    fat: float
    sodium: float
    sugars: float
    coles: float
    transfat: float

    class Config:
        orm_mode = True


@router.get("/{food_id}")
def user_get(
        food_id: int,
        session: Session = Depends(get_session)
) -> Food:
    food: m.Food | None = session.execute(
        sql_exp
        .select(m.Food)
        .where(m.Food.id == food_id)
    ).scalar_one_or_none()

    return Food.from_orm(food)
