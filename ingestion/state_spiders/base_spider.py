import logging
from abc import ABC, abstractmethod
from typing import List, Dict

logger = logging.getLogger(__name__)

class BaseStateSpider(ABC):
    """
    Abstract base class for all state-level politician and trade scrapers.
    Enforces a standard contract for data extraction across all 50 states.
    """
    def __init__(self, state_code: str):
        self.state_code = state_code.upper()

    @abstractmethod
    def fetch_officials(self) -> List[Dict]:
        """
        Must be implemented by subclasses to fetch state officials (Governors, State Senators, Assembly members).
        Returns a list of dictionaries matching the Politician model schema.
        """
        pass

    @abstractmethod
    def fetch_disclosures(self) -> List[Dict]:
        """
        Must be implemented by subclasses to fetch financial disclosures/trades for state officials.
        Returns a list of dictionaries matching the Trade model schema.
        """
        pass

    def normalize_name(self, raw_name: str) -> str:
        """
        Utility method to standardize names.
        """
        # Basic cleanup; can be overridden or expanded
        return " ".join(raw_name.split())
