import psycopg2
from credentials import master_username, master_password, endpoint, dbname

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host = endpoint,
            port = '5432',
            dbname = dbname,
            user = master_username,
            password = master_password
        )

        # cursor object
        cur = connection.cursor()

        # sample query
        cur.execute("""SELECT * FROM vendors""")
        query_results = cur.fetchall()
        print(query_results)

        # close cursor and connection
        cur.close()
        connection.close()

    except Exception as e:
        print(f"An error occurred: {e}")

connect_to_db()
