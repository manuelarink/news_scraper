import vcr
import requests
import pytest
from src.rssreader import RSSNewsReader
from src.news_scraper import NewsScraper


# TODO... hier weiter testen
# TODO: Tests mit verschiedenen Parametern von fetch
# TODO: Test bei fehlerhafter URL
# TODO: Test bei nicht konformem Inhalt des RSS-Files (anderer Struktur)
# TODO: Test bei ungültigem Startdatum
# TODO weitere Szenarien...
@pytest.mark.rss_news_reader
def test_fetch_valid_url_start_time_none_with_stub(request, monkeypatch, input_news_item):
    """
    Tests fetching and processing of rss-Content by patching request.get
    given a list of valid urls and no start_time.
    :return: None
    """

    class StubResponse(object):
        """
        Stub response for monkey-patching Http-Request in RssReader
        """
        def __init__(self, content):
            self.status_code = 200
            self.content = content

    def get_stub(*args, **kwargs):
        with open('news_rss.xml', 'r', encoding='utf-8') as rss_file:
            content = rss_file.read()
        return StubResponse(content)

    # using monkeypatch to replace call to http request
    monkeypatch.setattr(requests, 'get', get_stub)

    # Test, ob erstes item dem gewünschten Ergebnis entspricht
    rssreader = RSSNewsReader()
    for news_item in rssreader.fetch(NewsScraper.SOURCES):
        #print('iterating over generator')
        #print(f'generated NewsItem\n{news_item}')
        #print(f'expected NewsItem\n {input_news_item}')
        assert news_item == input_news_item
        break


@pytest.mark.vcr
@vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
def test_fetch_with_vcr():
    """
    Tests fetch function with vcr, patches http-requests by automatically capturing responses and storing
    them into a YAML file to be replayed during the tests.
    Note: The first time you run the test use
    pytest -k test_request_feed_with_vcr --record-mode=once
    :return:
    """
    news_reader = RSSNewsReader()
    for news_item in news_reader.fetch(NewsScraper.SOURCES):
        # retrieve the first article (item) from NewsScraper, then break
        print(news_item)
        # at least date and source should be set
        assert news_item.date and news_item.source
        break



