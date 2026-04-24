from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class USCode(Base):
    __tablename__ = 'us_code'

    id = Column(Integer, primary_key=True)
    title = Column(Integer, nullable=False)
    title_name = Column(String)
    chapter = Column(String)
    section = Column(String)
    text = Column(Text)

class Statute(Base):
    __tablename__ = 'statutes'

    id = Column(Integer, primary_key=True)
    public_law_number = Column(String, unique=True, index=True)
    name = Column(String)
    summary = Column(Text)
