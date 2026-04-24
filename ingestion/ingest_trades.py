import logging
import os
import sys
from datetime import datetime
import hashlib
import time

project_dir = "/content/TheLazarusPoliticianPortfolioTrackerByMrCakes931"
if project_dir not in sys.path:
    sys.path.append(project_dir)

from core.database import SessionLocal
from models.trades import Trade
from models.issuers import Issuer
from models.politicians import Politician
from data_sources.capitol_trades_api import CapitolTradesAPI
from data_sources.quiverquant_api import QuiverQuantAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_or_create_unknown_issuer(db):
    unknown_issuer = db.query(Issuer).filter(Issuer.ticker == "UNKNOWN").first()
    if not unknown_issuer:
        unknown_issuer = Issuer(ticker="UNKNOWN", name="Company UNKNOWN", sector="Unknown", industry="Unknown")
        db.add(unknown_issuer)
        db.commit()
        db.refresh(unknown_issuer)
        logger.info("Created UNKNOWN placeholder issuer.")
    return unknown_issuer

def ingest_trades():
    db = SessionLocal()
    unknown_issuer = get_or_create_unknown_issuer(db)
    issuers_in_db = db.query(Issuer).all()
    issuer_map = {issuer.ticker: issuer.id for issuer in issuers_in_db if issuer.ticker}

    politicians_in_db = db.query(Politician).all()
    politician_map = {pol.external_id: pol.id for pol in politicians_in_db if pol.external_id}
    politician_name_map = {pol.full_name: pol.id for pol in politicians_in_db if pol.full_name}

    default_politician = db.query(Politician).first()
    if not default_politician:
        logger.error("No politicians found in DB. Cannot ingest trades.")
        db.close()
        return
    default_politician_id = default_politician.id

    capitol_api = CapitolTradesAPI()
    quiver_api = QuiverQuantAPI()
    all_raw_trades = []

    try:
        logger.info("Fetching House trading data from QuiverQuant...")
        house_trades = quiver_api.get_house_trading()
        if house_trades:
            for trade_item in house_trades:
                # Corrected f-string with escaped internal quotes
                unique_id_str = f"{trade_item.get('BioGuideID', '')}-{trade_item.get('Date', '')}-{trade_item.get('Ticker', '')}-{trade_item.get('Transaction', '')}-{time.time()}"
                external_trade_id = hashlib.sha256(unique_id_str.encode()).hexdigest()

                politician_id = politician_map.get(trade_item.get('BioGuideID'))
                if not politician_id and trade_item.get('Representative'):
                    politician_id = politician_name_map.get(trade_item['Representative'])
                
                if not politician_id:
                    politician_id = default_politician_id

                # Data normalization for amounts
                amt_min, amt_max = 0.0, 0.0
                if trade_item.get('Amount'):
                    try:
                        clean_amt = str(trade_item['Amount']).replace('$', '').replace(',', '')
                        if '-' in clean_amt:
                            s_min, s_max = clean_amt.split('-')
                            amt_min = float(s_min.strip())
                            amt_max = float(s_max.strip())
                        else:
                            amt_min = float(clean_amt)
                            amt_max = float(clean_amt)
                    except Exception:
                        pass

                all_raw_trades.append({
                    'external_trade_id': external_trade_id,
                    'politician_id': politician_id,
                    'ticker': trade_item.get('Ticker'),
                    'trade_type': trade_item.get('Transaction'),
                    'trade_amount_min': amt_min,
                    'trade_amount_max': amt_max,
                    'trade_date': trade_item.get('Date'),
                    'disclosure_date': trade_item.get('last_modified'),
                    'source_system': 'QuiverQuant'
                })
    except Exception as e:
        logger.error(f"QuiverQuant fetch error: {e}")

    try:
        for item in all_raw_trades:
            ticker = item.get('ticker', 'UNKNOWN')
            issuer_id = issuer_map.get(ticker, unknown_issuer.id)

            # Date Parsing
            try:
                t_date = datetime.strptime(str(item['trade_date']), '%Y-%m-%d').date()
                d_date = datetime.strptime(str(item['disclosure_date']), '%Y-%m-%d').date()
                days_diff = (d_date - t_date).days
            except Exception:
                t_date, d_date, days_diff = None, None, None

            trade = db.query(Trade).filter(Trade.external_trade_id == item['external_trade_id']).first()
            if not trade:
                trade = Trade(
                    external_trade_id=item['external_trade_id'],
                    politician_id=item['politician_id'],
                    issuer_id=issuer_id,
                    trade_date=t_date,
                    disclosure_date=d_date,
                    days_until_disclosure=days_diff,
                    trade_type=item['trade_type'],
                    trade_amount_min=item['trade_amount_min'],
                    trade_amount_max=item['trade_amount_max'],
                    source_system=item['source_system']
                )
                db.add(trade)
            else:
                # Fix: Removed trailing commas to avoid tuple assignments
                trade.trade_type = item['trade_type']
                trade.trade_amount_min = item['trade_amount_min']
                trade.trade_amount_max = item['trade_amount_max']
                trade.value_at_purchase = 0.0
        db.commit()
        logger.info(f"Ingested {len(all_raw_trades)} trades successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction loop error: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    ingest_trades()
