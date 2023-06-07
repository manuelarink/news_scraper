import pytest
from rssreader import NewsItem
from dateutil.parser import parse

@pytest.fixture()
def input_news_item():
    """
    Returns an instance of NewsItem which is equal to the first NewsItem generated from the testfile news_rss.xml.
    :return:
    """
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
