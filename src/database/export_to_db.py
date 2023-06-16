from src.database.db_helper import export_csv_to_db
from pathlib import Path
import os

DEFAULT_DATABASE_URL = {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}
DEFAULT_DATA_DIR = {'data_dir': Path(f'{os.path.dirname(os.path.dirname(__file__))}/../data/')}


def export_data():
    '''
    Runs the db export.
    :return:
    '''
    export_csv_to_db(DEFAULT_DATABASE_URL, DEFAULT_DATA_DIR['data_dir'])


if __name__ == '__main__':
    export_data()

