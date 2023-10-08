from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from datetime import datetime
from typing import Optional  
from fastapi.responses import JSONResponse
from getdb import get_db, AddUser,UpdateUser
import logging
router=APIRouter()
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@router.post("/users/")
def create_user(info: AddUser, db: Session = Depends(get_db)):
    db_user = models.User(username=info.username, email=info.email, user_code=info.user_code,
                           date_of_creation=info.date_of_creation, date_of_birth=info.date_of_birth)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}")
def read_user(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    db_user = db.query(models.User).filter_by(id=user_id).all()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/")
def delete_user_by_code(user_code: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if user_code is None:
            raise HTTPException(status_code=400, detail="User code is required")
        db_user = db.query(models.User).filter_by(user_code=user_code).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.exception("An error occurred during user deletion")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})



@router.put("/users/")
def update_user_by_code(user_code: str, update_data: UpdateUser, db: Session = Depends(get_db)):
    try:
        if user_code is None:
            raise HTTPException(status_code=400, detail="User code is required")
        db_user = db.query(models.User).filter_by(user_code=user_code).first()
        if db_user:
            if update_data.username is not None:
                db_user.username = update_data.username
            if update_data.email is not None:
                db_user.email = update_data.email
            if update_data.date_of_birth is not None:
                db_user.date_of_birth = update_data.date_of_birth
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.exception("An error occurred during user update")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})

app.include_router(router, prefix="/api")