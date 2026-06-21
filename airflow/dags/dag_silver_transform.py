"""
DAG: dag_silver_transform
Runs dbt to build the Silver layer (staging and dimension models).
Triggered after dag_bronze_ingestion completes successfully.
"""

from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

from airflow import DAG

default_args = {
    "owner": "KyberCorax",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_silver_transform",
    description="Builds Silver layer dbt models after Bronze ingestion",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["silver", "dbt"],
) as dag:
    wait_for_bronze = ExternalTaskSensor(
        task_id="wait_for_bronze_ingestion",
        external_dag_id="dag_bronze_ingestion",  # watch this DAG
        external_task_id="quality_gate_bronze",  # wait for this specific task
        timeout=3600,  # give up after 1 hour (3600 seconds)
        poke_interval=60,  # check every 60 seconds
        mode="poke",  # keep checking repeatedly
    )

    run_silver_dbt = BashOperator(
        task_id="run_silver_dbt_models",
        bash_command=(
            "cd /opt/airflow/dbt/corax_arcana && "  # go into the dbt project folder
            # run only models tagged 'silver'
            # tell dbt where profiles.yml lives
            "dbt run --select tag:silver --profiles-dir /opt/airflow/dbt/corax_arcana"
        ),
    )

    quality_gate_silver = BashOperator(
        task_id="quality_gate_silver",
        bash_command=(
            "cd /opt/airflow/dbt/corax_arcana && "
            "dbt test --select tag:silver "
            "--profiles-dir /opt/airflow/dbt/corax_arcana"
        ),
    )

    wait_for_bronze >> run_silver_dbt >> quality_gate_silver
