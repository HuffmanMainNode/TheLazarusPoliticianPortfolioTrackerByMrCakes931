import logging
from core.database import SessionLocal
from models.trades import Trade

logger = logging.getLogger(__name__)

def ingest_trades(data: list):
    db = SessionLocal()
    try:
        for item in data:
            trade = db.query(Trade).filter(Trade.external_trade_id == item.get('external_trade_id')).first()
            if not trade:
                trade = Trade(**item)
                db.add(trade)
            else:
                for key, value in item.items():
                    setattr(trade, key, value)
        db.commit()
        logger.info(f"Successfully ingested {len(data)} trades.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting trades: {e}")
    finally:
        db.close()
