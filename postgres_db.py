import os
import subprocess

from credentials import master_username, master_password, endpoint, dbname
from helpers import create_csv_file


def copy_csv_to_db(data, csv_file_name, pk_columns):
    '''Converts a list of tuples to csv and copies the csv file to the 
    specified table in the database'''
    table_name = csv_file_name.split('/')[-1].split('.csv')[0]
    csv_file_name = create_csv_file(data, csv_file_name)

    commands = [
        f"DROP TABLE IF EXISTS tmp_{table_name}",
        f"CREATE TABLE tmp_{table_name} AS SELECT * FROM {table_name} LIMIT 0",
        f"\COPY tmp_{table_name} FROM '{csv_file_name}' CSV",
        f"INSERT INTO {table_name} SELECT * FROM tmp_{table_name} ON CONFLICT ({pk_columns}) DO NOTHING",
        f"DROP TABLE tmp_{table_name}",
    ]



    os.environ['PGPASSWORD'] = master_password

    for command in commands:
        psql_command = [
            'psql', '-h',
            endpoint,
            '-p',
            '5432',
            '-U',
            master_username,
            '-d',
            dbname,
            '-c',
            command
        ]

        process = subprocess.Popen(psql_command, stdout=subprocess.PIPE)
        process.wait()

    return process.stdout.read()

