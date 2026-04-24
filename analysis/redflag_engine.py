import logging
from core.database import SessionLocal
from models.trades import Trade
from models.red_flags import RedFlag
from models.politicians import Politician
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)

class RedFlagEngine:
    def __init__(self):
        self.db = SessionLocal()

    def check_timing_rules(self, trade):
        # Timing rules: late disclosure
        if trade.days_until_disclosure and trade.days_until_disclosure > 45:
            self._create_red_flag(trade, "LATE_DISCLOSURE", 3, f"Trade disclosed {trade.days_until_disclosure} days after execution.")
        
        # Simulated pre-legislation trade rule
        if trade.trade_amount_max and trade.trade_amount_max > 500000:
            self._create_red_flag(trade, "PRE_LEGISLATION_SUSPICION", 4, "Large trade executed potentially before legislation or hearing.")

    def check_sector_conflicts(self, trade):
        # Sector conflict rules: committee-sector conflict
        politician = self.db.query(Politician).options(joinedload(Politician.committees)).filter_by(id=trade.politician_id).first()
        if politician and trade.issuer and trade.issuer.sector:
            for committee in politician.committees:
                if trade.issuer.sector.lower() in committee.name.lower():
                    self._create_red_flag(trade, "COMMITTEE_SECTOR_CONFLICT", 5, f"Traded in {trade.issuer.sector} while on {committee.name}.")

    def check_pattern_rules(self, trade):
        # Pattern rules: clustered trades
        if trade.trade_type == "Purchase" and trade.trade_amount_min and trade.trade_amount_min >= 100000:
            self._create_red_flag(trade, "CLUSTERED_TRADES", 2, "High volume purchase pattern detected.")

    def check_network_rules(self, trade):
        # Network rules: PAC-to-trade linkage
        pass

    def _create_red_flag(self, trade, rule_code, severity, description):
        red_flag = RedFlag(
            politician_id=trade.politician_id,
            trade_id=trade.id,
            rule_code=rule_code,
            severity=severity,
            description=description
        )
        self.db.add(red_flag)

    def run_analysis(self):
        try:
            self.db.query(RedFlag).delete()
            self.db.commit()
            
            trades = self.db.query(Trade).options(joinedload(Trade.issuer)).all()
            for trade in trades:
                self.check_timing_rules(trade)
                self.check_sector_conflicts(trade)
                self.check_pattern_rules(trade)
                self.check_network_rules(trade)
            self.db.commit()
            logger.info(f"Red-flag analysis complete. Scanned {len(trades)} trades.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during red-flag analysis: {e}")
        finally:
            self.db.close()

if __name__ == '__main__':
    engine = RedFlagEngine()
    engine.run_analysis()
