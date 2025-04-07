import pytest
import psycopg2

@pytest.fixture(scope="session")
def temp_database_ini(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    ini_file = temp_dir / "database.ini"
    ini_file.write_text("""
[postgresql]
host=localhost
user=postgres
password=PsP99case*QIWI
port=5432
""")
    return ini_file

@pytest.fixture(scope="session")
def db_connection(temp_database_ini):
    from config import config
    params = config(filename=str(temp_database_ini))
    conn = psycopg2.connect(**params)
    yield conn
    conn.close()
