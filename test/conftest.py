import pytest
import os
import src.database.export_to_db as export
from src.rssreader import NewsItem
from dateutil.parser import parse
from pathlib import Path
from src.database import db_helper


@pytest.fixture(params=[{'database_url': 'sqlite:///headlines_test.db'},
                        {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}],
                ids=['test', 'production'])
def setup_db_connected(request):
    '''
    Parametrized fixture for establishing a connection to a db.
    :param request:
    :return:
    '''
    con = db_helper.connect(**request.param)
    yield con
    db_helper.disconnect(con)


@pytest.fixture(params=[{'database_url': 'sqlite:///headlines_test.db'},
                        {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}],
                ids=['test', 'production'])
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
    Fixture for setting up a test postgres-db.
    :return:
    '''
    # connect
    test_db_url = {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news_test'}
    con = db_helper.connect(**test_db_url)
    # drop table headlines if exists
    sql = 'DROP TABLE IF EXISTS headlines; DROP SEQUENCE IF EXISTS headlines_seq'
    con.engine.execute(sql)
    yield con
    # disconnect
    db_helper.disconnect(con)


@pytest.fixture()
def input_csv_dir_path():
    '''
    Fixture that return path-object to directory of test-csv.files.
    :return:
    '''
    return Path(f'{os.path.dirname(os.path.dirname(__file__))}/test/sample_data/')


@pytest.fixture(params=['test/sample_data/news-2023-06-06_12-40-37.csv',
                        'test/sample_data/news-2023-06-07_12-03-19.csv'],
                ids=['news-2023-06-06_12-40-37.csv',
                     'news-2023-06-07_12-03-19.csv'])
def input_data(request):
    '''
    Fixture that returns a dataframe containing the input of a csv-file stored in and csv_file_path.
    :return:
    '''
    csv_file_path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/{request.param}')
    return db_helper.load_data(csv_file_path), csv_file_path


@pytest.fixture(params=['test/sample_data/news-2022-08-04_12-16-50.csv'],
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
