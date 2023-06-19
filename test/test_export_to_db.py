import pytest
import src.database.export_to_db as export
import src.database.import_to_df as importdf
import os
import logging
from pathlib import Path


LOGGER = logging.getLogger(__name__)

@pytest.mark.test_export
def test_export(monkeypatch):
    '''
    Tests the export function for storing .csv-Data to database.
    :return:
    '''
    LOGGER.info('enter')

    # patch database connection and path for using test-sqlite-database and sample-data-directory
    LOGGER.info('patch exportDEFAULT_DATABASE_URL and export.DEFAULT_DATA_DIR')
    monkeypatch.setitem(export.DEFAULT_DATABASE_URL, 'database_url', 'sqlite:///headlinestest.db')
    monkeypatch.setitem(export.DEFAULT_DATA_DIR, 'data_dir', Path(f'{os.path.dirname(os.path.dirname(__file__))}/test/config/'))

    # do the export
    LOGGER.info('call export')
    export.export_data()

    # patch database connection for import function
    LOGGER.info('patch importdf.DEFAULT_DATABASE_URL')
    monkeypatch.setitem(importdf.DEFAULT_DATABASE_URL, 'database_url', 'sqlite:///headlinestest.db')

    # load data from db to check if export was successful
    LOGGER.info('import exported data to verify success')
    dataframe = importdf.import_data()
    LOGGER.info(f'{len(dataframe.index)} rows read')

    # TODO check properties of dataframe
    assert len(dataframe.index) > 0
