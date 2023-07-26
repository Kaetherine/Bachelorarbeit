from sqlalchemy import create_engine, text
import psycopg2
from credentials import master_username, master_password, endpoint, dbname
import pandas as pd

import csv
import os
import subprocess

# Erstellen Sie zuerst eine CSV-Datei aus Ihren Daten
fake_data = [
    ('Germany', 897.4),
    ('France', 458.7),
    ('United Kingdom', 423.2),
    ('Italy', 402.3),
    ('Spain', 333.1),
    ('Poland', 320.9),
    ('Netherlands', 196.3),
    ('Belgium', 119.3),
    ('Sweden', 55.1),
    ('Austria', 78.7),
    ('Greece', 71.1),
    ('Portugal', 59.3),
    ('Denmark', 42.8),
    ('Finland', 53.6),
    ('Ireland', 39.1),
]

csv_file = 'fake_data.csv'
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fake_data)

table_name = 'co2country'
copy_command = fr'''\COPY {table_name} FROM '/home/katherine/Development/Bachelorarbeit/{csv_file}' CSV'''

os.environ['PGPASSWORD'] = master_password
command = ['psql', '-h', endpoint, '-p', '5432', '-U', master_username, '-d', dbname, '-c', copy_command]

process = subprocess.Popen(command, stdout=subprocess.PIPE)
process.wait()
print(process.returncode)

output = process.stdout.read()
print(output)


# fake_data = [
#     ('Germany', 2023, 897.4),
#     ('France', 2023, 458.7),
#     ('United Kingdom', 2023, 423.2),
#     ('Italy', 2023, 402.3),
#     ('Spain', 2023, 333.1),
#     ('Poland', 2023, 320.9),
#     ('Netherlands', 2023, 196.3),
#     ('Belgium', 2023, 119.3),
#     ('Sweden', 2023, 55.1),
#     ('Austria', 2023, 78.7),
#     ('Greece', 2023, 71.1),
#     ('Portugal', 2023, 59.3),
#     ('Denmark', 2023, 42.8),
#     ('Finland', 2023, 53.6),
#     ('Ireland', 2023, 39.1),
# ]

# sql_command = '''INSERT INTO test (pk, colum1) VALUES ('es funktiniert', 'doch');'''

# os.environ['PGPASSWORD'] = master_password
# command = ['psql', '-h', endpoint, '-p', '5432', '-U', master_username, '-d', dbname, '-c', sql_command]

# process = subprocess.Popen(command, stdout=subprocess.PIPE)
# process.wait()
# print(process.returncode)

# output = process.stdout.read()
# print(output)



# import subprocess

# sql_command = '''INSERT INTO test (pk, colum1) VALUES ('hallo', 'tschuess');'''

# command = f'''
#     export PGPASSWORD='{master_password}'; 
#     psql -h {endpoint} -p 5432 -U {master_username} -d {dbname} -c "{sql_command}" '''

# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
# process.wait()
# print(process.returncode)

# output = process.stdout.read()
# print(output)

# def connect_to_db():
#     engine = create_engine(
#     f'''postgresql://
#     {master_username}:{master_password}
#     @{endpoint}:5432/{dbname}'''
#     )
#     return engine

# def test_connection(engine):
#     try:
#         with engine.connect() as connection:
#             result = connection.execute('select * from test')
#             print(f"Connection successful: {result.scalar() == 1}")
#     except Exception as e:
#         print(f"Connection failed: {e}")

# data = {
#     'name': ['Alice', 'Bob', 'Charlie'],
#     'age': [25, 45, 35],
#     'city': ['New York', 'Los Angeles', 'Chicago']
# }

# df = pd.DataFrame(data)
# db_connection = connect_to_db()

# df.to_sql('my_table', db_connection, if_exists='replace')
# import subprocess

# sql_command = '''INSERT INTO test (pk, colum1) VALUES ('hallo', 'tschuess');'''

# command = f'''
#     export PGPASSWORD='{master_password}'; 
#     psql -h {endpoint} -p 5432 -U {master_username} -d {dbname} -c "{sql_command}" '''

# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
# process.wait()
# print(process.returncode)

# output = process.stdout.read()
# print(output)


