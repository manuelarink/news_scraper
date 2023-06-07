import pytest
from rssreader import NewsItem
from dateutil.parser import parse
from database import db_store

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
