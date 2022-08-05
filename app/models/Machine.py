import datetime
from sqlalchemy import JSON, Column, Integer, Float, String, DateTime
from .database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    temperature = Column(Integer)
    sensor_a = Column(Integer)
    sensor_b = Column(Integer)
    status = Column(Integer)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    class Config:
        arbitrary_types_allowed = True
