"""
API Wrapper for Capitol Trades
Authoritative Source: Capitol Trades (https://www.capitoltrades.com)
"""
import requests
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class CapitolTradesAPI:
    BASE_URL = "https://api.capitoltrades.com/v1"

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.headers = {"Accept": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def _request(self, endpoint: str, params: Dict = None, retries: int = 3) -> Optional[Dict]:
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    logger.warning(f"Rate limited. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"HTTP error occurred: {e}")
                    break
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error occurred: {e}")
                time.sleep(2 ** attempt)
        return None

    def get_all_politicians(self, page: int = 1) -> List[Dict]:
        data = self._request("politicians", params={"page": page})
        return data.get('data', []) if data else []

    def get_trades_by_politician(self, politician_id: str) -> List[Dict]:
        data = self._request(f"politicians/{politician_id}/trades")
        return data.get('data', []) if data else []

    def get_latest_trades(self, limit: int = 100) -> List[Dict]:
        data = self._request("trades", params={"pageSize": limit})
        return data.get('data', []) if data else []
