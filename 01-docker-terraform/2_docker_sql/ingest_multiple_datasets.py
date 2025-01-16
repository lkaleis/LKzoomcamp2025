#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from time import time

def ingest_data(user, password, host, port, db, table_name, url):
    # the backup file is gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv(csv_name)

    # For datetime columns (if they exist), convert them
    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Convert the dataframe to SQL
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')  # Create the table structure
    df.to_sql(name=table_name, con=engine, if_exists='append')  # Insert data

    print(f"Data from {url} ingested into table {table_name}")

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name1 = params.table_name1
    table_name2 = params.table_name2
    table_name3 = params.table_name3  
    url1 = params.url1
    url2 = params.url2
    url3 = params.url3  

    # Ingest data from the first CSV (with datetime columns)
    ingest_data(user, password, host, port, db, table_name1, url1)

    # Ingest data from the second CSV (simple table with no datetime columns)
    ingest_data(user, password, host, port, db, table_name2, url2)

    # Ingest data from the third CSV (simple table with no datetime columns)
    ingest_data(user, password, host, port, db, table_name3, url3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name1', required=True, help='name of the first table')
    parser.add_argument('--url1', required=True, help='url of the first csv file')
    parser.add_argument('--table_name2', required=True, help='name of the second table')
    parser.add_argument('--url2', required=True, help='url of the second csv file')
    parser.add_argument('--table_name3', required=True, help='name of the third table')  
    parser.add_argument('--url3', required=True, help='url of the third csv file')  

    args = parser.parse_args()

    main(args)
