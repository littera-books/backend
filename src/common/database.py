from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .read_secrets import secret_json

DB_NAME = secret_json['DB_NAME']
DB_USER = secret_json['DB_USER']
HOST = secret_json['HOST']
PASSWORD = secret_json['PASSWORD']

engine = create_engine(
    f'postgresql://{DB_USER}:{PASSWORD}@{HOST}/{DB_NAME}', echo=False)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
