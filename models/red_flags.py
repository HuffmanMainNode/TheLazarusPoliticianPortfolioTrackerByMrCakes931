from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class RedFlag(Base):
    __tablename__ = 'red_flags'
    
    id = Column(Integer, primary_key=True)
    politician_id = Column(Integer, ForeignKey('politicians.id'), nullable=False)
    trade_id = Column(Integer, ForeignKey('trades.id'))
    rule_code = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    politician = relationship("Politician", back_populates="red_flags")
    trade = relationship("Trade", back_populates="red_flags")
