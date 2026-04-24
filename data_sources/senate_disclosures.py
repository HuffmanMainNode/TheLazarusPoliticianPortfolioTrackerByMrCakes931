import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class SenateDisclosuresAPI:
    def __init__(self):
        self.base_url = "https://efdsearch.senate.gov/search/"
        self.home_url = f"{self.base_url}home/"
        self.auth_url = f"{self.base_url}"
        self.data_url = f"{self.base_url}report/data/"
        self.session = requests.Session()

    def _agree_to_tos(self) -> bool:
        try:
            # Fetch initial CSRF token
            response = self.session.get(self.home_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
            
            # Submit TOS agreement
            payload = {
                'csrfmiddlewaretoken': csrf_token,
                'prohibition_agreement': '1'
            }
            headers = {
                'Referer': self.home_url,
                'User-Agent': 'Mozilla/5.0'
            }
            post_response = self.session.post(self.home_url, data=payload, headers=headers, timeout=10)
            return post_response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to agree to Senate TOS: {e}")
            return False

    def fetch_recent_disclosures(self) -> List[Dict]:
        logger.info("Fetching live Senate disclosures...")
        trades = []
        
        if not self._agree_to_tos():
            logger.error("Senate TOS agreement failed. Cannot fetch data.")
            return trades
            
        try:
            # Setup the search payload for Periodic Transaction Reports (PTRs)
            payload = {
                'start': 0,
                'length': 100,
                'report_types': '[11]', # 11 corresponds to PTRs
                'filer_types': '[]',
                'submitted_start_date': '01/01/2026 00:00:00',
                'submitted_end_date': ''
            }
            headers = {
                'Referer': f"{self.base_url}search/",
                'User-Agent': 'Mozilla/5.0',
                'X-CSRFToken': self.session.cookies.get('csrftoken', '')
            }
            
            response = self.session.post(self.data_url, data=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('data', []):
                first, last = item[0], item[1]
                ptr_link = item[3]
                date_received = item[4]
                
                trades.append({
                    'external_trade_id': f"S-{ptr_link}",
                    'politician_ext_id': f"{first} {last}",
                    'ticker': 'UNKNOWN',
                    'trade_type': 'Unknown',
                    'trade_amount_min': 0.0,
                    'trade_amount_max': 0.0,
                    'trade_date': '2026-01-01',
                    'disclosure_date': date_received,
                    'source_system': 'eSenate_Live_Scraper'
                })
            logger.info(f"Parsed {len(trades)} disclosure metadata records from Senate portal.")
        except Exception as e:
            logger.error(f"Failed to fetch Senate data: {e}")
            
        return trades
