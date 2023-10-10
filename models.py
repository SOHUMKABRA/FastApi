

from sqlalchemy import Column, Integer, String , Boolean, ForeignKey , DateTime
from database import Base
from datetime import datetime
class User(Base):
    __tablename__='Employee'
    id = Column(Integer, primary_key=True,index=True)
    username=Column(String , index=True)
    email=Column(String , index=True)
    user_code=Column(String, index=True)
    date_of_birth=Column(DateTime)
    date_of_creation=Column(DateTime, default=datetime.now())