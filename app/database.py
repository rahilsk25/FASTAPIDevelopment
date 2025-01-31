from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor


SQLALCHEMY_DATABASE_URL= f'postgresql://{settings.database_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_dbname}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn=psycopg2.connect(host="localhost", dbname="fastapi", user="postgres", password="Rskrahil786")
#         cur=conn.cursor()
#         print("Database connected successfully!!!")
#         break
#     except Exception as e:
#         print("Database connection failed!!!")
#         print("Error :", e)
#         time.sleep(3)