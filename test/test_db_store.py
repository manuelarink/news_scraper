import pytest
import sqlalchemy
import pandas as pd
from database import db_store


@pytest.mark.db_store
def test_connect_to_db_successful(setup_db_connected):
    '''
    Test on successful connecting to db.
    :param setup_db:
    :return:
    '''
    assert type(setup_db_connected) == sqlalchemy.engine.base.Connection


@pytest.mark.db_store
def test_disconnect_to_db_successful(setup_db_disconnected):
    '''
    Test on successful disconnecting from db.
    :param setup_db:
    :return:
    '''
    assert setup_db_disconnected.closed


@pytest.mark.db_store
def test_load_data_successful(input_data):
    '''
    Test on successful loading of csv-file into a dataframe.
    :return:
    '''
    dataframe, csv_file_path = input_data
    assert type(dataframe) == pd.DataFrame


@pytest.mark.db_store
def test_load_data_content_valid(input_data):
    '''
    Test on valid content and structure of dataframe.
    :return:
    '''
    dataframe, csv_file_path = input_data
    # assert columns are correctly set
    assert all(dataframe.columns == ['Date', 'Title', 'Description',
                                           'Author', 'Category', 'Copyright',
                                           'Url', 'Text', 'Source'])

    # assert number of rows corresponds to number of lines in csv
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        nmb_rows = len(file.readlines())
    assert len(dataframe.index) == nmb_rows


@pytest.mark.db_store
def test_get_dataframe_from_csv_concat_successful(input_csv_dir_path):
    '''
    Test on successful creation of a concatenated dataframe of all csv-Files in input_csv_dir.
    :param input_csv_dir:
    :return:
    '''
    # TODO: Tests on correct structure and content of dataframe
    df = db_store.get_dataframe_from_csv_dir(input_csv_dir_path)
    assert type(df) == pd.DataFrame


@pytest.mark.skip(reason='test not really of interest - just as example')
@pytest.mark.db_store
@pytest.mark.parametrize('database_url',
                         ['unknown_dialect+psycopg2://news:news@localhost:5432/news',
                          'postgresql+unknown_dbapi://news:news@localhost:5432/news',
                          'postgresql+psycopg2://unknown_user:news@localhost:5432/news',
                          'postgresql+psycopg2://news:unknown_pwd@localhost:5432/news',
                          'postgresql+psycopg2://news:news@unknown_host:5432/news]',
                          #'postgresql+psycopg2://news:news@localhost:0/news',
                          'postgresql+psycopg2://news:news@localhost:5432/unknown_db'])
def test_connect_to_db_fails(database_url):
    '''
    Test on failure establishing connection.
    :param database_url:
    :return:
    '''
    with pytest.raises(sqlalchemy.exc.SQLAlchemyError):
        con = db_store.connect(**{'database_url': database_url})
