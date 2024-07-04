from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('.')
from config import POSTGRE_PWD, POSTGRE_USER

DATABASE_URL = f"postgresql://{POSTGRE_USER}:{POSTGRE_PWD}@localhost:5432/datas"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
