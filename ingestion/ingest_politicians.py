import logging
from core.database import SessionLocal
from models.politicians import Politician

logger = logging.getLogger(__name__)

def ingest_politicians(data: list):
    db = SessionLocal()
    try:
        for item in data:
            pol = db.query(Politician).filter(Politician.external_id == item.get('external_id')).first()
            if not pol:
                pol = Politician(**item)
                db.add(pol)
            else:
                for key, value in item.items():
                    setattr(pol, key, value)
        db.commit()
        logger.info(f"Successfully ingested {len(data)} politicians.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting politicians: {e}")
    finally:
        db.close()
