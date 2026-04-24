from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Committee(Base):
    __tablename__ = 'committees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chamber = Column(String)
    code = Column(String, unique=True, index=True)
    
    politicians = relationship("Politician", secondary="politician_committees", back_populates="committees")

class PoliticianCommittee(Base):
    __tablename__ = 'politician_committees'
    
    politician_id = Column(Integer, ForeignKey('politicians.id'), primary_key=True)
    committee_id = Column(Integer, ForeignKey('committees.id'), primary_key=True)
