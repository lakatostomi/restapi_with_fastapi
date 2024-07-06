from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('.')
from config import POSTGRES_PWD, POSTGRES_USER, POSTGRES_HOST, TABLE_ID

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{TABLE_ID}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
