import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class HouseDisclosuresAPI:
    def fetch_recent_disclosures(self) -> List[Dict]:
        logger.info("Simulating fetching House disclosures...")
        return [
            {
                'external_trade_id': 'H-1001',
                'politician_ext_id': 'P-H-01',
                'ticker': 'AAPL',
                'trade_type': 'Purchase',
                'trade_amount_min': 15001,
                'trade_amount_max': 50000,
                'trade_date': '2026-04-20',
                'disclosure_date': '2026-04-22',
                'source_system': 'eHouse'
            }
        ]
