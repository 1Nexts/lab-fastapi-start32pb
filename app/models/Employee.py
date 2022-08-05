import datetime
from sqlalchemy import JSON, Column, Integer, Float, String, DateTime
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(256), unique=True)
    phone = Column(String(20))
    gender = Column(String(1))
    province_id = Column(Integer)
    date_of_birth = Column(DateTime)
    stack_interest = Column(JSON)
    note = Column(String(256))
    image = Column(String(256))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    class Config:
        arbitrary_types_allowed = True
