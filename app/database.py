from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import time

import psycopg2
from psycopg2.extras import RealDictCursor

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}/{3}".format(settings.p2eguildadm_user,settings.p2eguildadm_pass,settings.p2eguildadm_host,settings.p2eguildadm_dbname )


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all classes are an extension of this base class
Base = declarative_base()


# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database= 'p2eguildadm', user="guildmaster", password='<enterPassword>', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
    
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)




