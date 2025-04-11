import psycopg2
from typing import List, Dict, Any


def create_database(database_name: str, params):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) not null,
                employer_area VARCHAR(255) not null,
                employer_url TEXT,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER,
                vacancy_name VARCHAR(255),
                vacancy_area VARCHAR(255),
                salary INTEGER,
                employer_id INTEGER REFERENCES employers(employer_id),
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()



def insert_data_to_database(data: List[Dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Загружает данные о работодателях и вакансиях в соответствующие таблицы базы данных.

    :param data: Список словарей с данными о работодателях и их вакансиях.
    :param database_name: Название базы данных.
    :param params: Параметры подключения к базе данных.
    """

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for employer in data:
            # Вставка данных о работодателе
            cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_area, employer_url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
            """, (
                employer['id'],
                employer['name'],
                employer['area']['name'],
                f"https://hh.ru/employer/{employer['id']}",
                employer['open_vacancies']
            ))

            # Вставка данных о вакансиях
            for vacancy in employer['vacancies']:
                salary = vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary'].get('from') else None

                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    vacancy['id'],
                    vacancy['name'],
                    employer['area']['name'],  # так как vacancy_area нет, берём area работодателя
                    salary,
                    employer['id'],
                    vacancy['alternate_url']
                ))

    conn.commit()
    conn.close()
