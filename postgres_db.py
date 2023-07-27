from credentials import master_username, master_password, endpoint, dbname
from helper_functions import create_csv_file
import os
import subprocess

def copy_csv_to_db(data, csv_file_name, table_name, primary_key_columns):
    csv_file_name = create_csv_file(data, csv_file_name)

    commands = [
        f"DROP TABLE IF EXISTS tmp_{table_name}",
        f"CREATE TABLE tmp_{table_name} AS SELECT * FROM {table_name} LIMIT 0",
        f"\COPY tmp_{table_name} FROM '{csv_file_name}' CSV",
        f"INSERT INTO {table_name} SELECT * FROM tmp_{table_name} ON CONFLICT ({primary_key_columns}) DO NOTHING",
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
