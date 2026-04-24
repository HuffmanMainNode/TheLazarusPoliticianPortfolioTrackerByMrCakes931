import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Lazarus Politician Portfolio Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest data')
    ingest_parser.add_argument('--all', action='store_true', help='Ingest all data')
    ingest_parser.add_argument('--trades', action='store_true', help='Ingest trades data')
    ingest_parser.add_argument('--politicians', action='store_true', help='Ingest politicians data')

    # Redflags command
    redflags_parser = subparsers.add_parser('redflags', help='Run red-flag engine')
    redflags_parser.add_argument('--run', action='store_true', help='Run analysis')

    # Score command
    score_parser = subparsers.add_parser('score', help='Run ranking engine')
    score_parser.add_argument('--all', action='store_true', help='Score all politicians')
    score_parser.add_argument('--politician', type=str, help='Score a specific politician by Full Name')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--politician', type=str, help='Export data for a specific politician by Full Name')

    args = parser.parse_args()

    if args.command == 'ingest':
        if args.all:
            logger.info("Ingesting all data...")
        elif args.trades:
            logger.info("Ingesting trades...")
        elif args.politicians:
            logger.info("Ingesting politicians...")
        else:
            ingest_parser.print_help()

    elif args.command == 'redflags':
        if args.run:
            from analysis.redflag_engine import RedFlagEngine
            logger.info("Running red-flag engine...")
            engine = RedFlagEngine()
            engine.run_analysis()
        else:
            redflags_parser.print_help()

    elif args.command == 'score':
        if args.all:
            from analysis.ranking_engine import RankingEngine
            logger.info("Scoring all politicians...")
            engine = RankingEngine()
            engine.run_ranking()
        elif args.politician:
            logger.info(f"Scoring politician: {args.politician}")
        else:
            score_parser.print_help()

    elif args.command == 'export':
        if args.politician:
            logger.info(f"Exporting data for politician: {args.politician}")
        else:
            export_parser.print_help()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
