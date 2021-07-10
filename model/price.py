from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from model import BaseModel, metadata, engine


class Price(BaseModel):
    __tablename__ = "t_price"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, index=True, unique=True)
    price = Column(Integer, nullable=False, default=0)
    last_price = Column(Integer, nullable=False, default=0)
    last_modify_date = Column(TIMESTAMP, default=datetime.now())