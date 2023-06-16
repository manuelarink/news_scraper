import pytest
import src.database.import_to_df as importdf
import os
from pathlib import Path


@pytest.mark.test_import
def test_import(monkeypatch):
    '''
    Tests the import function for loading data from db to dataframe.
    :param monkeypatch:
    :return:
    '''
    # patch database connection for using test-sqlite-database
    # TODO: maybe import_data() cannot find the database -> change path
    monkeypatch.setitem(importdf.DEFAULT_DATABASE_URL, 'database_url', 'sqlite:///headlines_test.db')

    # do the import
    df = importdf.import_data()
    print(df)

    # TODO: check properties of dataframe
    assert len(df.index) > 0
