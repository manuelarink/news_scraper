from src.rssreader import RSSNewsReader
import requests

sources = [
    {"source": "Focus", "url": "https://rss.focus.de/politik/"},
    {"source": "Focus", "url": "https://rss.focus.de/politik/ausland/"},
    {"source": "stern", "url": "https://www.stern.de/feed/standard/politik"},
    {"source": "Tagesschau", "url": "https://www.tagesschau.de/xml/rss2/"},
    {"source": "Welt", "url": "https://www.welt.de/feeds/topnews.rss"},
    {"source": "Zeit", "url": "https://newsfeed.zeit.de/index"},
    {"source": "taz", "url": "https://taz.de/!p4608;rss/"},
    {"source": "ZDF heute", "url": "https://www.zdf.de/rss/zdf/nachrichten"}
]


# TODO... hier weiter testen
# TODO: Tests mit verschiedenen Parametern von fetch
# TODO: Test bei fehlerhafter URL
# TODO: Test bei nicht konformem Inhalt des RSS-Files (anderer Struktur)
# TODO: Test bei ungültigem Startdatum
# TODO weitere Szenarien...
def test_fetch_valid_url_start_time_none_with_mock(monkeypatch, input_news_item):
    """
    Tests fetching and processing of rss-Content by mocking request.get
    given a list of valid urls and no start_time.
    :return: None
    """

    class MockResponse(object):
        """
        Mock response for monkey-patching Http-Request in RssReader
        """
        def __init__(self, content):
            self.status_code = 200
            self.content = content

    def mock_get(*args, **kwargs):
        with open('news_rss.xml', 'r', encoding='utf-8') as rss_file:
            content = rss_file.read()
        return MockResponse(content)

    # using monkeypatch to replace result of http request
    monkeypatch.setattr(requests, 'get', mock_get)

    # Test, ob erstes item dem gewünschten Ergebnis entspricht
    rssreader = RSSNewsReader()
    for news_item in rssreader.fetch(sources):
        #print('iterating over generator')
        #print(f'generated NewsItem\n{news_item}')
        #print(f'expected NewsItem\n {input_news_item}')
        assert news_item == input_news_item
        break


