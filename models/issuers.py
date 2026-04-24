from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Issuer(Base):
    __tablename__ = 'issuers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True, index=True)
    sector = Column(String)
    industry = Column(String)
    
    trades = relationship("Trade", back_populates="issuer")
