from sqlalchemy.schema import Column
from sqlalchemy.sql import sqltypes

from .base_ import ModelBase


class Diet(ModelBase):
    __tablename__="diet"

    id = Column(sqltypes.Integer, primary_key=True)
    user_id = Column(sqltypes.Integer, ForeignKey("user.id"))
    food_id = Column(sqltypes.Integer, ForeignKey("food.id"))
