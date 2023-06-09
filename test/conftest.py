import pytest
from rssreader import NewsItem
from dateutil.parser import parse
from pathlib import Path
import os
from database import db_store


@pytest.fixture(params=[{'database_url': 'sqlite:///headlines_test.db'},
                        {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}],
                ids=['mock', 'production'])
def setup_db_connected(request):
    '''
    Parametrized fixture for establishing a connection to a db.
    :param request:
    :return:
    '''
    con = db_store.connect(**request.param)
    yield con
    db_store.disconnect(con)


@pytest.fixture(params=[{'database_url': 'sqlite:///headlines_test.db'},
                        {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}],
                ids=['mock', 'production'])
def setup_db_disconnected(request):
    '''
    Parametrized fixture for disconnection from db.
    :param request:
    :return:
    '''
    con = db_store.connect(**request.param)
    db_store.disconnect(con)
    yield con


@pytest.fixture()
def setup_db_with_mock(request):
    """
    Fixture zum Herstellen einer Verbindung zu einer Test-Datenbank.
    :param request:
    :return:
    """
    mock_db_url = getattr(request.module, 'mock_db_url')
    con = db_store.connect(**mock_db_url)
    yield con
    db_store.disconnect(con)


@pytest.fixture()
def input_csv_dir_path():
    '''
    Fixture that return path-object to directory of test-csv.files.
    :return:
    '''
    return Path(f'{os.path.dirname(os.path.dirname(__file__))}/test/test_data/')


@pytest.fixture(params=['test/test_data/news-2023-06-06_12-40-37.csv'], ids=['news-2023-06-06_12-40-37.csv'])
def input_data(request):
    '''
    Fixture that returns a dataframe containing the input of a csv-file.
    :return:
    '''
    csv_file_path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/{request.param}')
    return db_store.load_data(csv_file_path), csv_file_path


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
