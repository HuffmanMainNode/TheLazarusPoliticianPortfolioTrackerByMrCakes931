"""
API Wrapper for QuiverQuant Congress Trading
Authoritative Source: QuiverQuant (https://www.quiverquant.com/congresstrading/)
"""
import requests
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class QuiverQuantAPI:
    BASE_URL = "https://api.quiverquant.com/beta"

    def __init__(self, token: str = "YOUR_TOKEN_HERE"):
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Token {token}"
        }

    def _request(self, endpoint: str, retries: int = 3) -> Optional[List[Dict]]:
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
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

    def get_senate_trading(self) -> List[Dict]:
        data = self._request("live/senatetrading")
        return data if data else []

    def get_house_trading(self) -> List[Dict]:
        data = self._request("live/housetrading")
        return data if data else []
