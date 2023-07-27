from http.client import HTTPException

from django.http import JsonResponse
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from rest_framework import status
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql_exp

from app import models as m
from app.utils.rdb import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


class login_user(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class signup_user(BaseModel):
    username: str
    password: str
    height: float
    weight: float
    gender: int

    class Config:
        orm_mode = True


@router.post("/signup")
def signup(item: signup_user, session: Session = Depends(get_session())) -> signup_user:
    instance: m.User | None = session.execute(
        sql_exp.select(m.User).where(m.User.username == item.username)).scalar_one_or_none()
    if instance is not None:
        raise HTTPException(status_code=400, detail="Username already taken")
    else:
        return JsonResponse(item, status=status.HTTP_201_CREATED)

'''
    if any(existing_user.username == item.username for existing_user in m.User):
        raise HTTPException(status_code=400, detail="Username already taken")
    else:
        return JsonResponse(item, status=status.HTTP_201_CREATED)
'''


@router.post("/login")
def login(item: login_user, session: Session = Depends(get_session())) -> login_user:
    instance: m.User | None = session.execute(
        sql_exp.select(m.User).where(m.User.username == item.username)).scalar_one_or_none()
    if instance is None:
        raise HTTPException(status_code=401, detail="Login denied")
    if instance.password is not item.password:
        raise HTTPException(status_code=401, detail="Login denied")

    return {"message": 'Login successful'}

    '''
    match_user = [u for u in m.User if u.username == item.username]
    if not matched_user:
        raise HTTPException(status_code=401, detail="Login denied")
    if item.password != match_user[0].password:
        raise HTTPException(status_code=401, detail="Login denied")

    return {"message": "Login successful"}
    '''
