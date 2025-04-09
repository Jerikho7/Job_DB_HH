import psycopg2


def create_database(database_name: str, params):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    print(f"Старая база данных '{database_name}' удалена (если существовала).")

    cur.execute(f"CREATE DATABASE {database_name}")
    print(f"Новая база данных '{database_name}' создана.")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) not null,
                description TEXT,
                employer_area VARCHAR(255) not null,
                employer_url TEXT,
                open_vacancies INTEGER
            )
        """)
        print("Таблица 'employers' успешно создана.")

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
        print("Таблица 'vacancies' успешно создана.")

    conn.commit()
    conn.close()
    print("Создание базы данных и таблиц завершено успешно!")
