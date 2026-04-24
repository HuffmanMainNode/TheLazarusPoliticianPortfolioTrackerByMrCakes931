import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class SEC_EdgarAPI:
    def fetch_form4_filings(self) -> List[Dict]:
        logger.info("Simulating fetching SEC Form 4 filings...")
        return [
            {
                'external_trade_id': 'SEC-3001',
                'politician_ext_id': 'P-E-01',
                'ticker': 'GOOGL',
                'trade_type': 'Sale',
                'trade_amount_min': 250000,
                'trade_amount_max': 500000,
                'trade_date': '2026-04-18',
                'disclosure_date': '2026-04-20',
                'source_system': 'SEC_EDGAR'
            }
        ]
