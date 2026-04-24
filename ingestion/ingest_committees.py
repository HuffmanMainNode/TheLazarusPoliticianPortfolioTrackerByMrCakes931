import logging
from core.database import SessionLocal
from models.committees import Committee

logger = logging.getLogger(__name__)

def ingest_committees(data: list):
    db = SessionLocal()
    try:
        for item in data:
            committee = db.query(Committee).filter(Committee.code == item.get('code')).first()
            if not committee:
                committee = Committee(**item)
                db.add(committee)
            else:
                for key, value in item.items():
                    setattr(committee, key, value)
        db.commit()
        logger.info(f"Successfully ingested {len(data)} committees.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting committees: {e}")
    finally:
        db.close()
