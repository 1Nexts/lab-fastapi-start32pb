from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Sqlite3
# SQLALCHEMY_DATABASE_URL = "sqlite:///./starter32.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
#                        "check_same_thread": False})

# MySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/starter32?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:aNrwlOvWxG@xxx.xxx.xxx.xxx:port/starter32?charset=utf8mb4"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:aNrwlOvWxG@localhost/starter32?charset=utf8mb4"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:aNrwlOvWxG@localhost/starter32?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)



# PostgresSQL
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/cmfaststock"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
