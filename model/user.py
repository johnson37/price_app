
from sqlalchemy import Column, Integer, String

from model import BaseModel, metadata, engine, db_session


class User(BaseModel):
    __tablename__ = "t_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, index=True, unique=True)
    pwd = Column(String(32), nullable=False)
    email_address = Column(String(32), nullable=True)
    phone = Column(String(32), nullable=True)
    status = Column(Integer, nullable=True)

    @classmethod
    def get_users(cls):
        return db_session.query(User).all()

    @classmethod
    def get_registerd_users(cls):
        return db_session.query(User).filter(User.status == 1).all()

    @classmethod
    def get_waiting_users(cls):
        return db_session.query(User).filter(User.status == 0).all()

    @classmethod
    def byusername(cls, user_name):
        return db_session.query(User).filter(User.name == user_name).first()
