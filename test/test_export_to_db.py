import pytest
import src.database.export_to_db as export
import src.database.import_to_df as importdf
import os
from pathlib import Path


@pytest.mark.test_export
def test_export(monkeypatch):
    '''
    Tests the export function for storing .csv-Data to database.
    :return:
    '''
    # patch database connection and path for using test-sqlite-database and sample-data-directory
    monkeypatch.setitem(export.DEFAULT_DATABASE_URL, 'database_url', 'sqlite:///headlines_test.db')
    monkeypatch.setitem(export.DEFAULT_DATA_DIR, 'data_dir', Path(f'{os.path.dirname(os.path.dirname(__file__))}/sample_data/'))

    # do the export
    export.export_data()

    # patch database connection for import function
    # TODO: maybe import_data() cannot find the database -> change path
    monkeypatch.setitem(importdf.DEFAULT_DATABASE_URL, 'database_url', 'sqlite:///headlines_test.db')

    # load data from db to check if export was successful
    dataframe = importdf.import_data()
    print(dataframe)

    # TODO check properties of dataframe
    assert len(dataframe.index) > 0
