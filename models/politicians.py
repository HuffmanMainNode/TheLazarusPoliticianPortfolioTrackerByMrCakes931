from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class Politician(Base):
    __tablename__ = 'politicians'
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    chamber = Column(String)
    party = Column(String)
    state_code = Column(String)
    state_name = Column(String)
    district = Column(String)
    date_of_birth = Column(Date)
    created_at = Column(DateTime, default=func.now())
    
    trades = relationship("Trade", back_populates="politician")
    committees = relationship("Committee", secondary="politician_committees", back_populates="politicians")
    red_flags = relationship("RedFlag", back_populates="politician")
    score = relationship("PoliticianScore", back_populates="politician", uselist=False)
