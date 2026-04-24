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

def fetch_judicial_data():
    # Simulating data fetching from Supreme Court and Federal Judiciary directories
    logger.info("Simulating data fetch from Supreme Court and US Courts...")
    return [
        {
            'external_id': 'JUD-001',
            'full_name': 'John Roberts',
            'chamber': 'Judicial',
            'party': 'None',
            'state_code': 'DC',
            'district': None,
            'date_of_birth': datetime.strptime('1955-01-27', '%Y-%m-%d').date()
        },
        {
            'external_id': 'JUD-002',
            'full_name': 'Clarence Thomas',
            'chamber': 'Judicial',
            'party': 'None',
            'state_code': 'DC',
            'district': None,
            'date_of_birth': datetime.strptime('1948-06-23', '%Y-%m-%d').date()
        },
        {
            'external_id': 'JUD-003',
            'full_name': 'Sonia Sotomayor',
            'chamber': 'Judicial',
            'party': 'None',
            'state_code': 'DC',
            'district': None,
            'date_of_birth': datetime.strptime('1954-06-25', '%Y-%m-%d').date()
        },
        {
            'external_id': 'JUD-004',
            'full_name': 'Elena Kagan',
            'chamber': 'Judicial',
            'party': 'None',
            'state_code': 'DC',
            'district': None,
            'date_of_birth': datetime.strptime('1960-04-28', '%Y-%m-%d').date()
        }
    ]

def ingest_judicials():
    db = SessionLocal()
    data = fetch_judicial_data()

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
        logger.info(f"Successfully ingested {len(data)} judicial officials.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting judicial officials: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_judicials()
