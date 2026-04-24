# API Reference

## CLI Commands
- `lazarus ingest --all`: Ingest all data from configured sources.
- `lazarus redflags --run`: Run the red-flag detection engine.
- `lazarus score --all`: Calculate scores for all politicians.

## Modules
- `data_sources.*`: API wrappers for external data.
- `ingestion.*`: ETL pipelines.
- `analysis.*`: Analytical engines for flags and scoring.
