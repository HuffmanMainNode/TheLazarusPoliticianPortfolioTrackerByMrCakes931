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

def fetch_state_data():
    # Simulating data fetching from state directories
    logger.info("Simulating data fetch from USA.gov and state legislatures...")
    return [
        {
            'external_id': 'STATE-001',
            'full_name': 'Gavin Newsom',
            'chamber': 'Governor',
            'party': 'Democrat',
            'state_code': 'CA',
            'district': None,
            'date_of_birth': datetime.strptime('1967-10-10', '%Y-%m-%d').date()
        },
        {
            'external_id': 'STATE-002',
            'full_name': 'Ron DeSantis',
            'chamber': 'Governor',
            'party': 'Republican',
            'state_code': 'FL',
            'district': None,
            'date_of_birth': datetime.strptime('1978-09-14', '%Y-%m-%d').date()
        },
        {
            'external_id': 'STATE-003',
            'full_name': 'Greg Abbott',
            'chamber': 'Governor',
            'party': 'Republican',
            'state_code': 'TX',
            'district': None,
            'date_of_birth': datetime.strptime('1957-11-13', '%Y-%m-%d').date()
        },
        {
            'external_id': 'STATE-004',
            'full_name': 'Kathy Hochul',
            'chamber': 'Governor',
            'party': 'Democrat',
            'state_code': 'NY',
            'district': None,
            'date_of_birth': datetime.strptime('1958-08-27', '%Y-%m-%d').date()
        }
    ]

def ingest_states():
    db = SessionLocal()
    data = fetch_state_data()

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
        logger.info(f"Successfully ingested {len(data)} state officials.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting state officials: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_states()
