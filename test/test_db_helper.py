import pytest
import pandas as pd
import sqlalchemy.engine
from sqlalchemy import inspect
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import SQLAlchemyError
from src.database import db_helper
from test.utils.util import get_csv_file_path, get_csv_nmb_of_rows, get_db_nmb_rows


@pytest.mark.db_helper
def test_connect_to_db_successful(setup_db_connected):
    '''
    Test on successful connecting to db.
    :param setup_db:
    :return:
    '''
    assert type(setup_db_connected) == Connection


@pytest.mark.db_helper
def test_disconnect_to_db_successful(setup_db_disconnected):
    '''
    Test on successful disconnecting from db.
    :param setup_db:
    :return:
    '''
    assert setup_db_disconnected.closed


@pytest.mark.db_helper
def test_load_data_successful(input_data):
    '''
    Test on successful loading of csv-file into a dataframe.
    :return:
    '''
    dataframe, csv_file_path = input_data
    assert type(dataframe) == pd.DataFrame


@pytest.mark.db_helper
def test_load_data_empty_input_file(input_no_content):
    '''
    Test on correct behavior in case of emtpy csv-files.
    :param input_no_content:
    :return:
    '''
    dataframe, csv_file_path = input_no_content
    with open(csv_file_path, 'r') as file:
        count_rows = len(file.readlines())
    assert dataframe.empty and count_rows == 0


@pytest.mark.db_helper
def test_load_data_content_valid(input_data):
    '''
    Test on valid content and structure of dataframe.
    :return:
    '''
    dataframe, csv_file_path = input_data
    print(f'dataframe={dataframe}, csv_file_path={csv_file_path}')

    # assert columns are correctly set
    assert all(dataframe.columns == ['date', 'title', 'description',
                                           'author', 'category', 'copyright',
                                           'url', 'text', 'source'])

    # assert correct row count
    df = pd.read_csv(csv_file_path, delimiter=';', quotechar='"', header=None)
    assert len(dataframe.index) == len(df.index)


@pytest.mark.db_helper
def test_get_dataframe_from_csv_concat_successful(input_csv_dir_path):
    '''
    Test on successful creation of a concatenated dataframe of all csv-Files in input_csv_dir.
    :param input_csv_dir:
    :return:
    '''
    df = db_helper.get_dataframe_from_csv_dir(input_csv_dir_path)
    assert type(df) == pd.DataFrame

    # assert columns are correctly set
    assert all(df.columns == ['date', 'title', 'description',
                              'author', 'category', 'copyright',
                              'url', 'text', 'source'])

    # assert row count of concatenated df is sum of row counts of single df's
    row_count = 0
    for csv_file_path in list(input_csv_dir_path.rglob('*.csv')):
        if csv_file_path.stat().st_size > 0:
            df_single = pd.read_csv(csv_file_path, delimiter=';', quotechar='"', header=None)
            row_count += len(df_single.index)
    assert len(df.index) == row_count


@pytest.mark.skip(reason='test not really of interest - just as example')
@pytest.mark.db_helper
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
    with pytest.raises(SQLAlchemyError):
        con = db_helper.connect(**{'database_url': database_url})


@pytest.mark.db_helper
def test_should_create_table_headlines(setup_test_postgres_db_connected):
    '''
    Test on function _create_table on postgres-db. Should create table headlines, if not already existing.
    Table should be successfully created.
    :return:
    '''
    con, db_url = setup_test_postgres_db_connected
    db_helper._replace_table(con.engine)
    assert inspect(con.engine).has_table('headlines')


@pytest.mark.db_helper
# TODO implement test
# - test if connection to db can't be established: should raise exception
# - test if csv-file is empty: should pass through without exception, no changes on table headlines - (x)
# - test if connection is established and csv-file contains data: should insert data into table headlines - (x)
def test_insert_csv_to_db_successful(setup_test_postgres_db_connected: sqlalchemy.engine.Connection):
    '''
    Test on successful inserting of csv-files into table headlines.
    :param setup_test_postgres_db_connected: fixture providing connection and url to test postgres db
    :return: None
    '''
    con, db_url = setup_test_postgres_db_connected
    csv_file = get_csv_file_path(empty=False)
    db_helper.insert_csv_to_db(db_url, csv_file)
    csv_nmb_rows = get_csv_nmb_of_rows(csv_file)
    db_nmb_rows = get_db_nmb_rows(con)
    assert csv_nmb_rows == db_nmb_rows


@pytest.mark.db_helper
def test_insert_csv_to_db_empty_file(setup_test_postgres_db_connected: sqlalchemy.engine.Connection):
    '''
    Test on correct behavior in case of empty csv-file. Should pass through without exception, no changes on
    table headlines.
    :param setup_test_postgres_db_connected: fixture providing connection and url to test postgres db
    :return: None
    '''
    con, db_url = setup_test_postgres_db_connected
    csv_file = get_csv_file_path(empty=True)
    db_helper.insert_csv_to_db(db_url, csv_file)
    csv_nmb_rows = get_csv_nmb_of_rows(csv_file)
    db_nmb_rows = get_db_nmb_rows(con)
    assert csv_nmb_rows == 0 and db_nmb_rows == 0




