import logging
import os
import sys
from datetime import datetime

# Ensure the project root is in the path to allow imports
project_dir = '/content/TheLazarusPoliticianPortfolioTrackerByMrCakes931'
if project_dir not in sys.path:
    sys.path.append(project_dir)

from core.database import SessionLocal
from models.politicians import Politician

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_executive_data():
    # Simulating data fetching from White House and USA.gov directories
    logger.info("Simulating data fetch from White House and USA.gov...")
    return [
        {
            'external_id': 'EXEC-001',
            'full_name': 'Joe Biden',
            'chamber': 'Executive',
            'party': 'Democrat',
            'state_code': 'DE',
            'district': None,
            'date_of_birth': datetime.strptime('1942-11-20', '%Y-%m-%d').date()
        },
        {
            'external_id': 'EXEC-002',
            'full_name': 'Kamala Harris',
            'chamber': 'Executive',
            'party': 'Democrat',
            'state_code': 'CA',
            'district': None,
            'date_of_birth': datetime.strptime('1964-10-20', '%Y-%m-%d').date()
        },
        {
            'external_id': 'EXEC-003',
            'full_name': 'Antony Blinken',
            'chamber': 'Executive',
            'party': 'Democrat',
            'state_code': 'NY',
            'district': None,
            'date_of_birth': datetime.strptime('1962-04-16', '%Y-%m-%d').date()
        },
        {
            'external_id': 'EXEC-004',
            'full_name': 'Janet Yellen',
            'chamber': 'Executive',
            'party': 'Democrat',
            'state_code': 'CA',
            'district': None,
            'date_of_birth': datetime.strptime('1946-08-13', '%Y-%m-%d').date()
        }
    ]

def ingest_executives():
    db = SessionLocal()
    data = fetch_executive_data()

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
        logger.info(f"Successfully ingested {len(data)} executive officials.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting executive officials: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_executives()
