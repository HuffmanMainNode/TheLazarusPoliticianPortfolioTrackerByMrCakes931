import logging
from core.database import SessionLocal
from models.issuers import Issuer

logger = logging.getLogger(__name__)

def ingest_issuers(data: list):
    db = SessionLocal()
    try:
        for item in data:
            issuer = db.query(Issuer).filter(Issuer.ticker == item.get('ticker')).first()
            if not issuer:
                issuer = Issuer(**item)
                db.add(issuer)
            else:
                for key, value in item.items():
                    setattr(issuer, key, value)
        db.commit()
        logger.info(f"Successfully ingested {len(data)} issuers.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting issuers: {e}")
    finally:
        db.close()
