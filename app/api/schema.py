from typing import Optional
from numpy import char
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    level: Optional[str] = "normal"

class Machine(BaseModel):
    id: Optional[int] = None
    name: str
    temperature: int
    sensor_a: int = 100
    sensor_b: int = 5
    status: int = 0

class Employee(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: str
    province_id: int
    date_of_birth: str
    stack_interest: Optional[list[str]]
    note: Optional[str] = ""
    image: str
