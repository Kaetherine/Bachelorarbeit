import psycopg2
from credentials import master_username, master_password, endpoint, dbname

def connect_to_db():
    connection = psycopg2.connect(
        host = endpoint,
        port = '5432',
        dbname = dbname,
        user = master_username,
        password = master_password
    )

        # cursor object
    cur = connection.cursor()
    return cur, connection

def disconnect_from_db(cur, connection):
     # close cursor and connection
    cur.close()
    connection.close()

        
# # sample query
# cur.execute("""SELECT * FROM vendors""")
# query_results = cur.fetchall()
# print(query_results)

