from sqlalchemy import create_engine, text
import psycopg2
from credentials import master_username, master_password, endpoint, dbname
import pandas as pd

import csv
import os
import subprocess

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
