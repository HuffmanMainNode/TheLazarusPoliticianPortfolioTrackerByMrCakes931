import logging
import pandas as pd
import requests
import urllib.parse
import io
from typing import List, Dict
from .base_spider import BaseStateSpider

logger = logging.getLogger(__name__)

class ArizonaSpider(BaseStateSpider):
    def __init__(self):
        super().__init__(state_code="AZ")
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    def generate_auth_checkpoint_links(self, name: str, chamber: str) -> List[str]:
        """
        Generates a minimum of 3 public resource links for the authentication checkpoint.
        """
        encoded_name = urllib.parse.quote(name)
        links = [
            f"https://ballotpedia.org/{encoded_name.replace('%20', '_')}",  # Ballotpedia Profile
            f"https://en.wikipedia.org/wiki/{encoded_name.replace('%20', '_')}", # Wikipedia Profile
            f"https://www.azleg.gov/memberroster/" # AZ Leg Official Roster
        ]
        return links

    def fetch_officials(self) -> List[Dict]:
        """
        Scrapes real elected officials for Arizona from public Wikipedia tables.
        """
        logger.info(f"[{self.state_code}] Fetching real state officials and generating authentication links...")
        officials = []
        try:
            # Scrape Arizona State Senate using requests to bypass 403
            senate_url = "https://en.wikipedia.org/wiki/Arizona_State_Senate"
            response = requests.get(senate_url, headers=self.headers)
            senate_tables = pd.read_html(io.StringIO(response.text))

            for df in senate_tables:
                if 'Party' in df.columns and any(col in df.columns for col in ['Member', 'Name', 'Senator']):
                    name_col = 'Member' if 'Member' in df.columns else ('Senator' if 'Senator' in df.columns else 'Name')
                    for _, row in df.iterrows():
                        clean_name = self.normalize_name(str(row[name_col]))
                        officials.append({
                            "external_id": f"AZ-SEN-{row.get('District', '')}",
                            "full_name": clean_name,
                            "chamber": "State Senate",
                            "party": str(row['Party']),
                            "state_code": self.state_code,
                            "district": str(row.get('District', '')),
                            "auth_checkpoint_resources": self.generate_auth_checkpoint_links(clean_name, "State Senate")
                        })
                    break

            # Scrape Arizona State House
            house_url = "https://en.wikipedia.org/wiki/Arizona_House_of_Representatives"
            response = requests.get(house_url, headers=self.headers)
            house_tables = pd.read_html(io.StringIO(response.text))

            for df in house_tables:
                if 'Party' in df.columns and any(col in df.columns for col in ['Member', 'Name', 'Representative']):
                    name_col = 'Member' if 'Member' in df.columns else ('Representative' if 'Representative' in df.columns else 'Name')
                    for _, row in df.iterrows():
                        clean_name = self.normalize_name(str(row[name_col]))
                        officials.append({
                            "external_id": f"AZ-HOU-{row.get('District', '')}",
                            "full_name": clean_name,
                            "chamber": "State House",
                            "party": str(row['Party']),
                            "state_code": self.state_code,
                            "district": str(row.get('District', '')),
                            "auth_checkpoint_resources": self.generate_auth_checkpoint_links(clean_name, "State House")
                        })
                    break
        except Exception as e:
            logger.error(f"[{self.state_code}] Error fetching real officials: {e}")

        return officials

    def fetch_disclosures(self) -> List[Dict]:
        """
        STRICT MANDATE: NO MOCK DATA. Returns empty until a verified live AZ disclosure API/scraper is built.
        """
        return []
