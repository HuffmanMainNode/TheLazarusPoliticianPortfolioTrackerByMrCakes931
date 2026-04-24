from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class PoliticianScore(Base):
    __tablename__ = 'politician_scores'
    
    politician_id = Column(Integer, ForeignKey('politicians.id'), primary_key=True)
    corruption_score = Column(Float)
    last_calculated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    politician = relationship("Politician", back_populates="score")
