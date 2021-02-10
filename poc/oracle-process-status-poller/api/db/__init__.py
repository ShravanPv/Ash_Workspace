from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
