from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.api import schema
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.User import User as UserDB
from app.api import security
from datetime import datetime, timedelta
from app.config.setting import settings
router = APIRouter()


@router.get("/authen")
def get_authen():
    return {"result": "authen"}


@router.post("/register")
def register(user: schema.User, db: Session = Depends(get_db)):

    try:
        user_db = UserDB(username=user.username,
                         password=security.get_password_hash(user.password))
        db.add(user_db)
        db.commit()
        return {
            "result": "ok",
            "detail": "Register success"}
    except Exception as e:
        print("error ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Duplicate username",
        )


@router.post("/login")
def login(user: schema.User, db: Session = Depends(get_db)):
    try:
        user_db = db.query(UserDB).filter(
            UserDB.username == user.username).first()

        # verify username
        if not user_db:
            raise HTTPException(
                status_code=404,
                detail="Invalid username",
            )
            # return {"result": "fail", "error": "invalide username"}

        # verify password
        if not security.verify_password(user.password, user_db.password):
            raise HTTPException(
                status_code=404,
                detail="Invalid password",
            )
            # return {"result": "fail", "error": "invalide password"}

        # create jwt token
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)

        # Remove some data
        user_db.password = ""
        # del user_db['password']

        # login success
        return {"result": "ok", 
                "token": token,
                "detail":"Login success",
                "user_db":user_db}
    except Exception as e:
        raise e
        # return {"result": "fail", "error": e}
