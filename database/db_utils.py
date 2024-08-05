import time
import os
import random
import string
import pytz
import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from schema import Base

def get_connection() -> Engine:
    """
    Authenticates to the DB and returns a Session.
    :return: Engine
    """
    try:
        # Establish an SQLite3 connection
        SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        return engine

    except Exception as connect_exception:
        print(f'Connection could not be made due to the following error: {repr(connect_exception)}')


def read_data(file_path: str) -> pd.DataFrame:
    """
    Reads data from the csv file and returns a Dataframe if successful or a str if not.
    :param: file_path: str
    :return: pd.DataFrame | str
    """
    try:
        df = pd.read_csv(file_path)
        return df

    except Exception as read_exception:
        print(f'Unable to access csv file, {repr(read_exception)}')


def create_tables() -> None:
    # connecting to SQLite3.
    engine = get_connection()
    # creating tables
    Base.metadata.create_all(engine)
    print(f'Successful in creating the tables')


def insert_data() -> None:
    """
    formats and inserts the csv file into the database.
    :return: None
    """
    # connecting to SQLite3.
    engine = get_connection()

    # to measure performance
    start_time = time.time()

    cwd = os.getcwd()
    # reading csv files
    store_status_df: pd.DataFrame = read_data(cwd+'/database/data/store_status.csv')
    time_zone_df: pd.DataFrame = read_data(cwd+'/database/data/time_zones.csv')
    menu_hours_df: pd.DataFrame = read_data(cwd+'/database/data/menu_hours.csv')

    merged_df = pd.merge(menu_hours_df, time_zone_df, on='store_id')

    # Function to convert local time to UTC
    def convert_to_utc(local_time_str, tz_str):
        local_tz = pytz.timezone(tz_str)
        local_time = pd.Timestamp(local_time_str).tz_localize(local_tz)
        return local_time.tz_convert(pytz.utc)

    # Apply the conversion function to the start_time_local and end_time_local columns
    merged_df['start_time_utc'] = merged_df.apply(
        lambda row: convert_to_utc(row['start_time_local'], row['timezone_str']), axis=1
    )

    merged_df['end_time_utc'] = merged_df.apply(
        lambda row: convert_to_utc(row['end_time_local'], row['timezone_str']), axis=1
    )

    # Convert the 'timestamp_column' to pandas Timestamp type if it's not already
    store_status_df['timestamp_utc'] = pd.to_datetime(store_status_df['timestamp_utc'], format='mixed')
    # Convert pandas datetime objects to SQL format (Y-M-D H:M:S)
    store_status_df['timestamp_utc'] = store_status_df['timestamp_utc'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # inserting data into the database.
    try:
        store_status_df.to_sql('store_status', con=engine, chunksize=10000, if_exists='replace', index=False)
        time_zone_df.to_sql('time_zone', con=engine, chunksize=10000, if_exists='replace', index=False)
        menu_hours_df.to_sql('menu_hours', con=engine, chunksize=10000, if_exists='replace', index=False)
        merged_df.to_sql('menu_hours_utc', con=engine, chunksize=10000, if_exists='replace', index=False)
    except Exception as insert_exception:
        print(f'Unable to populate tables, {repr(insert_exception)}')
    else:
        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        print(f'Successful in populating the tables in {execution_time:.2f} minutes')


def insert_dummy_data() -> None:
    dummy_data = []
    for _ in range(10):
        dummy_item = {
            'report_id': ''.join(random.choices(string.ascii_uppercase, k=10)),
            'store_id': random.randint(1, 100),
            'uptime_last_hour': random.randint(0, 60),
            'uptime_last_day': random.randint(0, 1440),
            'uptime_last_week': random.randint(0, 10080),
            'downtime_last_hour': random.randint(0, 60),
            'downtime_last_day': random.randint(0, 1440),
            'downtime_last_week': random.randint(0, 10080)
        }
        dummy_data.append(dummy_item)

    engine = get_connection()

    dummy_df = pd.DataFrame.from_records(dummy_data, nrows=10)
    dummy_df.to_sql('reports', con=engine, if_exists='replace', index=False)


if __name__ == "__main__":
    insert_data()
    # create_tables()
    # insert_dummy_data()
