from sqlalchemy.schema import Column
from sqlalchemy.sql import sqltypes

from .base_ import ModelBase


class User(ModelBase):
    __tablename__ = "user"

    id = Column(sqltypes.Integer, primary_key=True)

    username = Column(sqltypes.String, unique=True, nullable=False)
    password = Column(sqltypes.String, nullable=True)
