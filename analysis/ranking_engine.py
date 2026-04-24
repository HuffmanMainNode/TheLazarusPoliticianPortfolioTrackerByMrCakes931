import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
import random
from core.database import SessionLocal
from models.politicians import Politician
from models.red_flags import RedFlag
from models.scores import PoliticianScore

logger = logging.getLogger(__name__)

class RankingEngine:
    def __init__(self):
        self.db = SessionLocal()

    def calculate_score(self, red_flags):
        if not red_flags:
            return 0.0

        total_severity = sum(flag.severity for flag in red_flags)
        # Nonlinear scoring function to compress into 0-100 range
        score = 100 * (1 - math.exp(-0.1 * total_severity))
        return round(score, 2)
        
    def assign_tier(self, net_worth):
        if net_worth > 50000000:
            return "Tier 1 - Top Wealthiest"
        elif net_worth > 10000000:
            return "Tier 2 - Middle"
        else:
            return "Tier 3 - Bribery Risk"

    def run_ranking(self):
        try:
            politicians = self.db.query(Politician).all()
            for pol in politicians:
                # Get red flags for the politician
                red_flags = self.db.query(RedFlag).filter(RedFlag.politician_id == pol.id).all()
                score_val = self.calculate_score(red_flags)

                score_record = self.db.query(PoliticianScore).filter(PoliticianScore.politician_id == pol.id).first()
                if not score_record:
                    score_record = PoliticianScore(politician_id=pol.id, corruption_score=score_val)
                    self.db.add(score_record)
                else:
                    score_record.corruption_score = score_val
                
                # Determine wealth tier based on estimated net worth (simulated if unavailable)
                net_worth = getattr(pol, 'estimated_net_worth', None)
                if net_worth is None:
                    net_worth = random.uniform(1000000, 100000000)
                tier = self.assign_tier(net_worth)
                logger.info(f"Calculated for {pol.full_name}: {tier}, Corruption Score: {score_val}")

            self.db.commit()
            logger.info(f"Ranking complete. Updated scores and evaluated tiers for {len(politicians)} politicians.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during ranking analysis: {e}")
        finally:
            self.db.close()

if __name__ == '__main__':
    engine = RankingEngine()
    engine.run_ranking()
