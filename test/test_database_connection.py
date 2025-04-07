def test_database_connection(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        assert result[0] == 1
