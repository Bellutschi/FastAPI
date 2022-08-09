from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection string to database 'postgresql://<username>:<password>@<ip-address>/<hostname>/<database>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:kira@localhost/api'

# engine creates the connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# instance is a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# returns a class, which will be used to create models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()