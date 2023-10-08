from database import SessionLocal
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AddUser(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    user_code: Optional[str]
    date_of_birth: Optional[datetime]
    date_of_creation: Optional[datetime]

class UpdateUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    date_of_birth: Optional[datetime]