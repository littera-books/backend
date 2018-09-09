from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common import read_secrets

DB_NAME = read_secrets.secret_json['DB_NAME']
DB_USER = read_secrets.secret_json['DB_USER']
HOST = read_secrets.secret_json['HOST']
PASSWORD = read_secrets.secret_json['PASSWORD']

engine = create_engine(
    f'postgresql://{DB_USER}:{PASSWORD}@{HOST}/{DB_NAME}', echo=True)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
