from sqlalchemy import create_engine, text
import psycopg2
from credentials import master_username, master_password, endpoint, dbname

def connect_to_db():
    engine = create_engine(
        f'''postgresql+psycopg2://
        {master_username}:{master_password}
        @{endpoint}:5432/{dbname}'''
        )
    return engine

def test_connection(engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection successful: {result.scalar() == 1}")
    except Exception as e:
        print(f"Connection failed: {e}")

db_connection = connect_to_db()
test_connection(db_connection)
# DataFrame in die Datenbank schreiben
# df.to_sql('table_name', engine, if_exists='append', chunksize=500)

# def connect_to_db():
#     '''establishes the db connection and return
#     cursor and connection object'''
#     connection = psycopg2.connect(
#         host = endpoint,
#         port = '5432',
#         dbname = dbname,
#         user = master_username,
#         password = master_password
#     )

#         # cursor object
#     cur = connection.cursor()
#     return cur, connection

# def disconnect_from_db(cur, connection):
#     '''close cursor and connection'''
#     cur.close()
#     connection.close()

        
# # # sample query
# # cur.execute("""SELECT * FROM vendors""")
# # query_results = cur.fetchall()
# # print(query_results)

