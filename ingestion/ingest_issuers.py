import logging
import os
import sys
import yfinance as yf

project_dir = "/content/TheLazarusPoliticianPortfolioTrackerByMrCakes931"
if project_dir not in sys.path:
    sys.path.append(project_dir)

from core.database import SessionLocal
from models.issuers import Issuer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_issuers():
    db = SessionLocal()
    try:
        # Get all unique issuers from the database
        issuers = db.query(Issuer).filter(Issuer.ticker != "UNKNOWN").all()
        logger.info(f"Found {len(issuers)} unique issuers to resolve.")

        for issuer in issuers:
            ticker_symbol = issuer.ticker
            if not ticker_symbol:
                continue

            logger.info(f"Fetching live data for: {ticker_symbol}")
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                
                # Handle cases where info might be empty or missing keys
                if info:
                    name = info.get("longName") or info.get("shortName") or issuer.name
                    sector = info.get("sector", "Unknown")
                    industry = info.get("industry", "Unknown")

                    # Update existing issuer record
                    issuer.name = name
                    issuer.sector = sector
                    issuer.industry = industry
                    logger.info(f"  -> Updated: {name} | Sector: {sector} | Industry: {industry}")
                else:
                    logger.warning(f"  -> No data found for {ticker_symbol} via yfinance.")

            except Exception as e:
                logger.error(f"  -> Error fetching data for {ticker_symbol}: {e}")

        db.commit()
        logger.info("Successfully updated issuer metadata from live sources.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error in issuer ingestion pipeline: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_issuers()
