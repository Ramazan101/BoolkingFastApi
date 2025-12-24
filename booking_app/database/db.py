from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DB_URL = 'postgresql+psycopg2://postgres:adminadmin@localhost/booking_app'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()