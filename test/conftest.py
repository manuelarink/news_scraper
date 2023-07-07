import pytest
import os

from bs4 import BeautifulSoup

from src.rssreader import NewsItem
from dateutil.parser import parse
from pathlib import Path
from src.database import db_helper

PG_TEST_DB_URL = {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news_test'}
SQLITE_TEST_DB_URL = {'database_url': 'sqlite:///headlinestest.db'}


@pytest.fixture(params=[PG_TEST_DB_URL, SQLITE_TEST_DB_URL],
                ids=['test-postgres', 'test-sqlite'])
def setup_db_connected(request):
    '''
    Parametrized fixture for establishing a connection to a db.
    :param request:
    :return:
    '''
    con = db_helper.connect(**request.param)
    yield con
    db_helper.disconnect(con)


@pytest.fixture(params=[PG_TEST_DB_URL, SQLITE_TEST_DB_URL],
                ids=['test-postgres', 'test-sqlite'])
def setup_db_disconnected(request):
    '''
    Parametrized fixture for disconnection from db.
    :param request:
    :return:
    '''
    con = db_helper.connect(**request.param)
    db_helper.disconnect(con)
    yield con


@pytest.fixture()
def setup_test_postgres_db_connected():
    '''
    Fixture for establishing a connection to a postgres-db for testing.
    Connects to database, clear table data and yield connection-object and url to postgres-db.
    Closes the connection after test.
    :return: connection-object, url to postgres-db
    :rtype: tuple
    '''
    # connect
    con = db_helper.connect(**PG_TEST_DB_URL)
    # drop table headlines if exists
    db_helper._replace_table(con.engine)
    yield con, PG_TEST_DB_URL
    # disconnect
    db_helper.disconnect(con)


@pytest.fixture()
def input_csv_dir_path():
    '''
    Fixture that return path-object to directory of test-csv.files.
    :return:
    '''
    return Path(f'{os.path.dirname(os.path.dirname(__file__))}/test/config/test_data_dir')


@pytest.fixture(params=['test/config/test_data_dir/news-2023-06-06_12-40-37.csv',
                        'test/config/test_data_dir/news-2023-06-07_12-03-19.csv'],
                ids=['news-2023-06-06_12-40-37.csv',
                     'news-2023-06-07_12-03-19.csv'])
def input_data(request):
    '''
    Fixture that returns a dataframe containing the input of a csv-file stored in and csv_file_path.
    :return:
    '''
    csv_file_path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/{request.param}')
    return db_helper.load_data(csv_file_path), csv_file_path


@pytest.fixture(params=['test/config/test_data_dir/news-2022-08-04_12-16-50.csv'],
                ids=['no-content: news-2022-08-04_12-16-50.csv'])
def input_no_content(request):
    '''
    Fixture for providing test-input when working with empty csv-files.
    :param request:
    :return:
    '''
    csv_file_path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/{request.param}')
    return db_helper.load_data(csv_file_path), csv_file_path


@pytest.fixture()
def input_news_item(request):
    """
    Returns an instance of NewsItem which is equal to the first NewsItem generated from the testfile news_rss.xml.
    :return:
    """
    print(f'\nFixture scope: {str(request.scope)}')
    print(f'\nCalling function: {str(request.function.__name__)}')
    print(f'\nCalling module: {str(request.module.__name__)}')

    return NewsItem(parse('Fri, 02 Jun 2023 12:18:20 +0200'),
                    'China hat dazu aufgerufen, keine weiteren Waffen mehr für den Konflikt zu liefern, '
                    'um den Krieg beenden zu können. Laut des Gouverneurs der russischen Grenzregion Belgorod '
                    'sind bei einem Angriff zwei Menschen getötet worden. Die Entwicklungen im Liveblog.',
                    'https://www.tagesschau.de/newsticker/liveblog-ukraine-freitag-268.html',
                    '',
                    'Liveblog: ++ China fordert Stopp von Waffenlieferungen ++',
                    '',
                    '',
                    '',
                    'Focus')


@pytest.fixture(params=['<item><pubDate>Fri, 02 Jun 2023 12:18:20 +0200</pubDate></item>',
                        '<item><pubDate>Fri, 02 Jun 2023 12:18:20 GMT</pubDate></item>',
                        '<item><pubDate>Fri, 2 Jun 2023 12:18:20 +0200</pubDate></item>',
                        '<item><pubDate>Fri, 2 Jun 23 12:18:20 +0200</pubDate></item>'])
def input_item_pubdate_varying(request):
    """
    Fixture for providing a BeautifulSoup
    :param request:
    :return:
    """
    soup = BeautifulSoup(request.param, 'lxml')
    return soup.item
