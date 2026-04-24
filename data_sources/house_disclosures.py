import logging
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class HouseDisclosuresAPI:
    def __init__(self):
        self.base_url = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/"
        self.current_year = datetime.now().year

    def fetch_recent_disclosures(self) -> List[Dict]:
        logger.info(f"Fetching live House disclosures for {self.current_year}...")
        zip_url = f"{self.base_url}{self.current_year}/{self.current_year}FD.zip"
        
        trades = []
        try:
            response = requests.get(zip_url, timeout=15)
            response.raise_for_status()
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                xml_filename = f"{self.current_year}FD.xml"
                if xml_filename in z.namelist():
                    with z.open(xml_filename) as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        
                        for member in root.findall('.//Member'):
                            last = member.findtext('Last')
                            first = member.findtext('First')
                            # This is a simplified extraction logic for the House XML structure
                            doc_id = member.findtext('DocID')
                            
                            # In a full implementation, you would use the DocID to download
                            # the specific PDF and parse the trades from it using PyPDF2 or pdfplumber.
                            # For now, we yield the metadata of the disclosure.
                            if doc_id:
                                trades.append({
                                    'external_trade_id': f"H-{doc_id}",
                                    'politician_ext_id': f"{first} {last}",
                                    'ticker': 'UNKNOWN',
                                    'trade_type': 'Unknown',
                                    'trade_amount_min': 0.0,
                                    'trade_amount_max': 0.0,
                                    'trade_date': '2026-01-01',
                                    'disclosure_date': datetime.now().strftime('%Y-%m-%d'),
                                    'source_system': 'eHouse_Live_XML'
                                })
            logger.info(f"Parsed {len(trades)} disclosure metadata records from House XML.")
        except Exception as e:
            logger.error(f"Failed to fetch or parse House XML: {e}")
            
        return trades
