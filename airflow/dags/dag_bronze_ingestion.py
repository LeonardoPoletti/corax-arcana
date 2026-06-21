"""
DAG: dag_bronze_ingestion
Featches Scryfall buck card data every day and writes it
as Parquet files into the Bronze layer
"""

from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator

from airflow import DAG

default_args = {
    "owner": "KyberCorax",  # label shown in the UI
    "retries": 1,  # if the task fails, try once more
    "retry_delay": timedelta(minutes=5),  # wait 5 minutes before retrying
}

with DAG(
    dag_id="dag_bronze_ingestion",  # unique name shown in the UI
    # human-readable description
    description="Daily ingestion of Scryfall bulk data into the Bronze layer",
    schedule="@daily",  # run once per day
    start_date=datetime(2025, 1, 1),  # DAG exists from this date
    catchup=False,  # don't run all missed days
    default_args=default_args,  # apply owner/retries to all tasks
    tags=["bronze", "ingestion"],  # labels for filtering in the UI
) as dag:
    ingest_scryfall_cards = BashOperator(
        task_id="ingest_scryfall_cards",  # name of this task
        bash_command=(
            "cd /opt/airflow && "  # go to the project root inside the container
            "BRONZE_PATH=data/bronze "  # tell the script where Bronze lives
            # tell the script where DuckDB lives
            "DUCKDB_PATH=data/corax_arcana.duckdb "
            "python src/ingestion/run.py"  # run your ingestion script
        ),
    )

    quality_gate_bronze = BashOperator(
        task_id="quality_gate_bronze",
        bash_command=(
            'python -c "'
            "import pathlib, sys; "
            "files = list(pathlib.Path('/opt/airflow/data/bronze').rglob('*.parquet'));"
            "print(f'Bronze quality gate: found {len(files)} Parquet files'); "
            "sys.exit(0) if files else sys.exit(1)"
            '"'
        ),
    )

    ingest_scryfall_cards >> quality_gate_bronze
