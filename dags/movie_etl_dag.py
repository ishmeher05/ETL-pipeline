from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2


# -------- EXTRACT --------
def extract():
    url = "https://api.tvmaze.com/shows"
    response = requests.get(url)
    data = response.json()

    return data[:5]


# -------- TRANSFORM --------
def transform(ti):
    data = ti.xcom_pull(task_ids='extract_task')

    cleaned_data = []

    for show in data:
        cleaned_data.append({
            "name": show.get("name"),
            "rating": show.get("rating", {}).get("average") or 0,
            "language": show.get("language")
        })

    return cleaned_data


# -------- LOAD --------
def load(ti):
    data = ti.xcom_pull(task_ids='transform_task')

    conn = psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            name TEXT,
            rating FLOAT,
            language TEXT
        )
    """)

    for movie in data:
        cur.execute("""
            INSERT INTO movies(name, rating, language)
            VALUES (%s, %s, %s)
        """, (
            movie["name"],
            movie["rating"],
            movie["language"]
        ))

    conn.commit()
    cur.close()
    conn.close()


# -------- DAG --------
with DAG(
    dag_id="movie_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load
    )

    extract_task >> transform_task >> load_task