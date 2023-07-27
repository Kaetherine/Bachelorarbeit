from credentials import master_username, master_password, endpoint, dbname
from helper_functions import create_csv_file
import csv
import os
import subprocess

def copy_csv_to_db(data, csv_file_name, table_name):
    '''docstring here'''
    csv_file_name = create_csv_file(data, csv_file_name)
    
    copy_command = fr'''\COPY {table_name} FROM '{csv_file_name}' CSV'''
    os.environ['PGPASSWORD'] = master_password
    command = [
        'psql', '-h',
        endpoint,
        '-p',
        '5432',
        '-U',
        master_username,
        '-d',
        dbname,
        '-c',
        copy_command
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()
    
    return process.stdout.read()
