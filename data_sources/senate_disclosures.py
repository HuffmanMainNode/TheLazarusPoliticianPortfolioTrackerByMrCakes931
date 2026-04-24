import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class SenateDisclosuresAPI:
    def fetch_recent_disclosures(self) -> List[Dict]:
        logger.info("Simulating fetching Senate disclosures...")
        return [
            {
                'external_trade_id': 'S-2001',
                'politician_ext_id': 'P-S-01',
                'ticker': 'MSFT',
                'trade_type': 'Sale',
                'trade_amount_min': 50001,
                'trade_amount_max': 100000,
                'trade_date': '2026-04-15',
                'disclosure_date': '2026-04-21',
                'source_system': 'eSenate'
            }
        ]
