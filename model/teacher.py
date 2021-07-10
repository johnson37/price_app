
from sqlalchemy import Column, Integer, String

from model import BaseModel


class Teacher(BaseModel):
    __tablename__ = "t_teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, index=True, unique=True)


