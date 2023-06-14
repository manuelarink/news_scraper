from db_store import export_csv_to_db
from pathlib import Path
import os


if __name__ == '__main__':
    database_url = {'database_url':
                    "postgresql+psycopg2://news:news@localhost:5432/news"}
    path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/../data/')
    export_csv_to_db(database_url, path)

