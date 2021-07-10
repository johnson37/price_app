from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

BaseModel = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:123456@127.0.0.1:5432/testdb', echo=True)
# 创建数据库表

db_session = sessionmaker(engine)()
metadata = BaseModel.metadata
