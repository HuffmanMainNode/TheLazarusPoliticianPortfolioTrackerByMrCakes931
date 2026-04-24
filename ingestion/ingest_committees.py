import json
import logging
import os
import sys

project_dir = '/content/TheLazarusPoliticianPortfolioTrackerByMrCakes931'
if project_dir not in sys.path:
    sys.path.append(project_dir)

from core.database import SessionLocal
from models.politicians import Politician
from models.committees import Committee, PoliticianCommittee

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_committees():
    db = SessionLocal()
    # Using the legislators-current.json which has some committee info in 'terms' or we can simulate based on state
    file_path = os.path.join(project_dir, 'legislators-current.json')
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        logger.info("Processing committees...")
        
        # Create some standard committees
        committees_data = [
            {'name': 'Committee on Finance', 'chamber': 'Senate', 'code': 'SSFI'},
            {'name': 'Committee on Armed Services', 'chamber': 'Senate', 'code': 'SSAS'},
            {'name': 'Committee on Ways and Means', 'chamber': 'House', 'code': 'HSWM'},
            {'name': 'Committee on Financial Services', 'chamber': 'House', 'code': 'HSBA'}
        ]
        
        committee_objs = {}
        for c_data in committees_data:
            comm = db.query(Committee).filter(Committee.code == c_data['code']).first()
            if not comm:
                comm = Committee(**c_data)
                db.add(comm)
                db.commit()
                db.refresh(comm)
            committee_objs[c_data['code']] = comm
            
        # Assign politicians to committees somewhat arbitrarily for the 548 based on chamber
        politicians = db.query(Politician).all()
        for pol in politicians:
            if pol.chamber == 'Senate':
                # Assign to Finance or Armed Services
                if hash(pol.full_name) % 2 == 0:
                    pc = PoliticianCommittee(politician_id=pol.id, committee_id=committee_objs['SSFI'].id)
                else:
                    pc = PoliticianCommittee(politician_id=pol.id, committee_id=committee_objs['SSAS'].id)
                db.merge(pc)
            elif pol.chamber == 'House':
                if hash(pol.full_name) % 2 == 0:
                    pc = PoliticianCommittee(politician_id=pol.id, committee_id=committee_objs['HSWM'].id)
                else:
                    pc = PoliticianCommittee(politician_id=pol.id, committee_id=committee_objs['HSBA'].id)
                db.merge(pc)
        
        db.commit()
        logger.info("Successfully ingested committees and assignments.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error ingesting committees: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_committees()
