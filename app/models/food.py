from sqlalchemy.schema import Column
from sqlalchemy.sql import sqltypes

from .base_ import ModelBase


class Food(ModelBase):
    __tablename__="food"
    id = Column(sqltypes.Integer, primary_key=True)
    name = Column(sqltypes.Integer, nullable=False)
    carbo = Column(sqltypes.Float, nullable=False)
    protein = Column(sqltypes.Float, nullable=False)
    fat = Column(sqltypes.Float, nullable=False)
    sodium = Column(sqltypes.Float, nullable=False)
    sugars = Column(sqltypes.Float, nullable=False)
    coles = Column(sqltypes.Float, nullable=False)
    transfat = Column(sqltypes.Float, nullable=False)