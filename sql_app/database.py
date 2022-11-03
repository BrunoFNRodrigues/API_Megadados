from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv   
import os
load_dotenv()                   

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")

SQLALCHEMY_DATABASE_URL = "mysql://{USER}:{PASSWORD}@localhost:3306/{DB}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine( SQLALCHEMY_DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
