import csv
import pandas as pd
import pandas.errors

import src.database.db_helper as db_helper
from pathlib import Path

PUBDATES_FILE_NAME = 'pubdates.csv'
CONFIG_DIR = 'config'
TEST_DATA_DIR = 'test_data_dir'

BASE_DIR = Path(__file__).resolve().parent.parent
PUBDATES_FILE = BASE_DIR.joinpath(CONFIG_DIR).joinpath(PUBDATES_FILE_NAME)

DB_NEWS_TABLE = 'headlines'


def get_pubdates() -> list:
    """
    Reads .csv - file containing different date formats in <pubdate> and returns the contents as list of tuple.
    :return:
    """
    with open(PUBDATES_FILE, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)    # skip the first line of csv (column names)
        data = [tuple(line) for line in csv_reader]
        return data


def get_csv_file_path(empty:bool = False) -> Path:
    """
    Returns the path to the test csv-file containing the news.
    :param empty: if True, the file will be empty
    :type empty: bool
    :return:
    :rtype: Path
    """
    if empty:
        return BASE_DIR / CONFIG_DIR / TEST_DATA_DIR / 'news-2022-08-04_12-16-50.csv'
    else:
        return BASE_DIR / CONFIG_DIR / TEST_DATA_DIR / 'news-2023-06-06_12-40-37.csv'


def get_csv_nmb_of_rows(csv_file: Path) -> int:
    """
    Returns the number of rows in the test csv-file containing the news.
    :param csv_file: path to the csv-file
    :return: number of rows in the csv-file
    :rtype: int
    """
    try:
        df = pd.read_csv(csv_file, sep=';', quotechar='"', header=None)
    except pandas.errors.EmptyDataError:
        return 0
    else:
        return len(df.index)


def get_db_nmb_rows(db_con) -> int:
    """
    Returns the number of rows in the database table.
    :param db_con: connection object to the database
    :return: number of rows in the database table
    :rtype: int
    """
    #df = pd.read_sql_table(DB_NEWS_TABLE, con.engine)
    df = pd.read_sql(sql='SELECT * FROM headlines', con=db_con)
    return len(df.index)


