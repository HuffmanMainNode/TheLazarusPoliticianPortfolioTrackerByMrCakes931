import logging
import os
import sys

project_dir = '/content/TheLazarusPoliticianPortfolioTrackerByMrCakes931'
if project_dir not in sys.path:
    sys.path.append(project_dir)

from core.database import SessionLocal, init_db
from models.legal import USCode, Statute

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_us_code():
    # Ensure tables are created
    init_db()
    db = SessionLocal()
    
    try:
        logger.info("Archiving U.S. Federal Laws (Simulated)...")
        
        # Simulated US Code data
        us_codes = [
            {'title': 18, 'title_name': 'Crimes and Criminal Procedure', 'chapter': '11', 'section': '201', 'text': 'Bribery of public officials and witnesses...'},
            {'title': 15, 'title_name': 'Commerce and Trade', 'chapter': '2B', 'section': '78j', 'text': 'Manipulative and deceptive devices (Insider Trading)...'}
        ]
        
        for uc_data in us_codes:
            uc = db.query(USCode).filter(USCode.title == uc_data['title'], USCode.section == uc_data['section']).first()
            if not uc:
                uc = USCode(**uc_data)
                db.add(uc)
                
        # Simulated Statutes data
        statutes = [
            {'public_law_number': 'Pub.L. 112-105', 'name': 'STOCK Act', 'summary': 'Stop Trading on Congressional Knowledge Act of 2012'}
        ]
        
        for st_data in statutes:
            st = db.query(Statute).filter(Statute.public_law_number == st_data['public_law_number']).first()
            if not st:
                st = Statute(**st_data)
                db.add(st)
                
        db.commit()
        logger.info("Successfully archived simulated U.S. Code and Statutes.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting U.S. federal laws: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_us_code()
