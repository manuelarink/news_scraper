import vcr
import requests
import pytest
from src.rssreader import RSSNewsReader
from src.news_scraper import NewsScraper


# TODO TEST for method request_feed
# feed_url not valid anymore - x
# feed_url provided, valid and can be retieved
@pytest.mark.rss_news_reader
def test_request_feed_url_not_valid():
    '''
    If url to request is wrong or not valid anymore uut (unit under test) should return None
    instead of raising Exception
    :return:
    '''
    assert RSSNewsReader.request_feed({"url": 'http://not-a-valid-resource.de/news.rss'}) is None


@pytest.mark.rss_news_reader
def test_request_feed_url_valid():
    '''
    Tests if response is correct when requesting a valid url.
    Type must be Response, StatusCode 200, content rss, url must correspond to call parameter
    (TODO We need to patch here (vcr))
    :return:
    '''
    url = 'https://rss.focus.de/politik/'
    response = RSSNewsReader.request_feed({'url': url})
    assert type(response) is requests.Response
    assert response.status_code == 200
    assert response.url == url
    assert response.text.startswith('<rss version="2.0"')


# TODO Test von fetch()
# TODO: Tests mit verschiedenen Parametern von fetch, Test bei fehlerhafter URL
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



