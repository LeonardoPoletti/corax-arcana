"""
DAG: dag_gold_aggregate
Runs dbt to build the Gold layer (fact and aggregate models).
Triggered after dag_silver_transform completes successfully.
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
    dag_id="dag_gold_aggregate",
    description="Builds Gold layer dbt models after Silver transform",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["gold", "dbt"],
) as dag:
    wait_for_silver = ExternalTaskSensor(
        task_id="wait_for_silver_transform",
        external_dag_id="dag_silver_transform",
        external_task_id="quality_gate_silver",
        timeout=3600,
        poke_interval=60,
        mode="poke",
    )

    run_gold_dbt = BashOperator(
        task_id="run_gold_dbt_models",
        bash_command=(
            "cd /opt/airflow/dbt/corax_arcana && "
            "DBT_BRONZE_PATH=/opt/airflow/data/bronze "
            "dbt run --select tag:gold --profiles-dir /opt/airflow/dbt/corax_arcana"
        ),
    )

    quality_gate_gold = BashOperator(
        task_id="quality_gate_gold",
        bash_command=(
            "cd /opt/airflow/dbt/corax_arcana && "
            "DBT_BRONZE_PATH=/opt/airflow/data/bronze "
            "dbt test --select tag:gold "
            "--profiles-dir /opt/airflow/dbt/corax_arcana"
        ),
    )

    wait_for_silver >> run_gold_dbt >> quality_gate_gold
