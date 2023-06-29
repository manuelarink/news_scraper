import csv
from pathlib import Path

PUBDATES_FILE_NAME = 'pubdates.csv'
CONFIG_FILE_DIR = 'config'

BASE_DIR = Path(__file__).resolve().parent.parent
PUBDATES_FILE = BASE_DIR.joinpath(CONFIG_FILE_DIR).joinpath(PUBDATES_FILE_NAME)


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

