from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models.base import Base
# Import all models so they are registered with Base metadata
from models.politicians import Politician
from models.issuers import Issuer
from models.trades import Trade
from models.committees import Committee, PoliticianCommittee
from models.red_flags import RedFlag
from models.scores import PoliticianScore
from models.legal import USCode, Statute

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///lazarus_politrack.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
