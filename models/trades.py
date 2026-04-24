from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    politician_id = Column(Integer, ForeignKey('politicians.id'), nullable=False)
    issuer_id = Column(Integer, ForeignKey('issuers.id'), nullable=False)
    external_trade_id = Column(String, unique=True, index=True)
    trade_date = Column(Date)
    disclosure_date = Column(Date)
    days_until_disclosure = Column(Integer)
    trade_type = Column(String)
    trade_amount_raw = Column(String)
    trade_amount_min = Column(Float)
    trade_amount_max = Column(Float)
    value_at_purchase = Column(Float)
    source_system = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    politician = relationship("Politician", back_populates="trades")
    issuer = relationship("Issuer", back_populates="trades")
    red_flags = relationship("RedFlag", back_populates="trade")
