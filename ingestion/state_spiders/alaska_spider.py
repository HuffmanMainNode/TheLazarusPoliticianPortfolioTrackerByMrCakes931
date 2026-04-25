import logging
import pandas as pd
from typing import List, Dict
from .base_spider import BaseStateSpider

logger = logging.getLogger(__name__)

class AlaskaSpider(BaseStateSpider):
    def __init__(self):
        super().__init__(state_code="AK")

    def fetch_officials(self) -> List[Dict]:
        """
        Scrapes real elected officials for Alaska from public Wikipedia tables.
        """
        logger.info(f"[{self.state_code}] Fetching real state officials from public records...")
        officials = []
        try:
            # Scrape Alaska State Senate
            senate_url = "https://en.wikipedia.org/wiki/Alaska_Senate"
            senate_tables = pd.read_html(senate_url)
            for df in senate_tables:
                if 'Party' in df.columns and any(col in df.columns for col in ['Member', 'Name', 'Senator']):
                    name_col = 'Member' if 'Member' in df.columns else ('Senator' if 'Senator' in df.columns else 'Name')
                    for _, row in df.iterrows():
                        officials.append({
                            "external_id": f"AK-SEN-{row.get('District', '')}",
                            "full_name": self.normalize_name(str(row[name_col])),
                            "chamber": "State Senate",
                            "party": str(row['Party']),
                            "state_code": self.state_code,
                            "district": str(row.get('District', ''))
                        })
                    break

            # Scrape Alaska State House
            house_url = "https://en.wikipedia.org/wiki/Alaska_House_of_Representatives"
            house_tables = pd.read_html(house_url)
            for df in house_tables:
                if 'Party' in df.columns and any(col in df.columns for col in ['Member', 'Name', 'Representative']):
                    name_col = 'Member' if 'Member' in df.columns else ('Representative' if 'Representative' in df.columns else 'Name')
                    for _, row in df.iterrows():
                        officials.append({
                            "external_id": f"AK-HOU-{row.get('District', '')}",
                            "full_name": self.normalize_name(str(row[name_col])),
                            "chamber": "State House",
                            "party": str(row['Party']),
                            "state_code": self.state_code,
                            "district": str(row.get('District', ''))
                        })
                    break
        except Exception as e:
            logger.error(f"[{self.state_code}] Error fetching real officials: {e}")
            
        return officials

    def fetch_disclosures(self) -> List[Dict]:
        """
        STRICT MANDATE: NO MOCK DATA. Returns empty until a verified live API is connected.
        """
        return []
