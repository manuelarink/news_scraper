import datetime
import requests
import pytest
from bs4 import BeautifulSoup
from src.rssreader import RSSNewsReader, NewsItem
from src.news_scraper import NewsScraper
from test.utils.util import get_pubdates


# Test cases for method test_request_feed_url:
# - feed_url not valid anymore - x
# - feed_url provided, valid and can be retieved - x
@pytest.mark.rss_news_reader
def test_request_feed_url_not_valid():
    """
    If url to request is wrong or not valid anymore uut (unit under test) should return None
    instead of raising Exception
    :return:
    """
    assert RSSNewsReader.request_feed({"url": 'http://not-a-valid-resource.de/news.rss'}) is None


@pytest.mark.rss_news_reader
@pytest.mark.vcr
def test_request_feed_url_valid():
    """
    Tests if response is correct when requesting a valid url. Request is patched to guarantee that valid resource
    at given url exists.
    Type must be Response, StatusCode 200, content rss, url must correspond to call parameter
    Note: The first time you run the test use
    pytest -k test_request_feed_url_valid --record-mode=once
    :return:
    """
    url = 'https://rss.focus.de/politik/'
    response = RSSNewsReader.request_feed({'url': url})
    assert type(response) is requests.Response
    assert response.status_code == 200
    assert response.url == url
    assert response.text.startswith('<rss version="2.0"')


# Test cases for method create_news_item(article_date: datetime.datetime, feed_url: dict, item: bs4.element.Tag) -> NewsItem
# - item is None: should raise exception - x
# - item contains malformed data (expected child-tags and attributes missed): should raise exception - x (skipped because not useful)
# - item is valid: should return NewsItem with attributes corresponding to item-content - x
@pytest.mark.rss_news_reader
def test_create_news_item_item_none():
    """
    If no item is provided, uut should raise TypeError
    :return:
    """
    with pytest.raises(TypeError):
        RSSNewsReader.create_news_item(datetime.datetime.now(), {'url': 'https://rss.focus.de/politik/'}, None)


@pytest.mark.skip(reason='skipped because not really useful (test evaluates api behaviour)')
@pytest.mark.rss_news_reader
def test_create_news_item_item_malformed():
    """
    If item does not contain expected child tags and attributes to create NewsItem from,
    uut should raise AttributeError.
    :return:
    """
    def get_malformed_item_stub():
        with open('config/malformed_item.xml', 'r') as file:
            soup = BeautifulSoup(file.read(), 'lxml')
            return soup.find('item')

    with pytest.raises(AttributeError):
        RSSNewsReader.create_news_item(datetime.datetime.now(),
                                       {'url': 'https://rss.focus.de/politik/', 'source': 'Focus'},
                                       get_malformed_item_stub())


# Test cases for method get_item_date(item: bs4.element.Tag) -> datetime.datetime
# - item is None - should raise exception - x
# - item is malformed (contains no 'pubdate') - should raise exception - not implemented, not useful
# - item is valid:
#   test pubdate with different date format - should parse correctly and
#   return correct datetime corresponding to 'pubdate' in item - x
@pytest.mark.rss_news_reader
def test_get_item_date_item_none():
    """
    If no item is provided, uut should raise TypeError
    :return:
    """
    with pytest.raises(TypeError):
        RSSNewsReader.get_item_date(None)


@pytest.mark.rss_news_reader
@pytest.mark.parametrize('item, expect_day, expect_month, expect_year, expect_hour, expect_minute, expect_second',
                         get_pubdates())
def test_get_item_date_on_dateformat(item, expect_day, expect_month, expect_year,
                                     expect_hour, expect_minute, expect_second):
    """
    Test on valid item with different dateformats. Should parse without errors
    and return correct datetime.
    :return:
    """
    soup = BeautifulSoup(item, 'lxml')
    article_date = RSSNewsReader.get_item_date(soup.item)
    assert type(article_date) == datetime.datetime
    assert article_date.year == int(expect_year)
    assert article_date.month == int(expect_month)
    assert article_date.day == int(expect_day)
    assert article_date.hour == int(expect_hour)
    assert article_date.minute == int(expect_minute)
    assert article_date.second == int(expect_second)


@pytest.mark.rss_news_reader
def test_create_news_item_successful():
    """
    Tests if input item is ok - should return a NewsItem with corresponding attributes.
    :return:
    """
    def get_item_stub():
        with open('config/valid_item.xml', 'r') as file:
            soup = BeautifulSoup(file.read(), 'lxml')
            return soup.find('item')

    date = datetime.datetime.now()
    feed_url = {'url': 'https://rss.focus.de/politik/', 'source': 'Focus'}
    news_item = RSSNewsReader.create_news_item(date,
                                               feed_url,
                                               get_item_stub())
    assert type(news_item) == NewsItem
    assert news_item.date == date
    assert news_item.source == feed_url['source']
    assert news_item.url == 'https://www.tagesschau.de/wirtschaft/technologie/ki-boom-100.html'
    assert news_item.title == 'Welche Firmen besonders vom KI-Boom profitieren'
    assert news_item.description == 'Tech-Unternehmen konnten in den vergangenen Wochen vom Boom in der KI-Branche ' \
                                    'profitieren. Allerdings gibt es Unterschiede - ' \
                                    'und ein Unternehmen sticht besonders hervor.'
    assert news_item.copyright == ''
    assert news_item.category == ''
    assert news_item.author == ''


# TODO Test von fetch()
# TODO: Tests mit verschiedenen Parametern von fetch, Test bei fehlerhafter URL
# TODO: Test bei nicht konformem Inhalt des RSS-Files (anderer Struktur)
# TODO: Test bei ungültigem Startdatum
# TODO weitere Szenarien...
@pytest.mark.rss_news_reader
def test_fetch_valid_url_start_time_none_with_stub(monkeypatch, input_news_item):
    """
    Tests fetching and processing of rss-Content by patching request.get
    given a list of valid urls and no start_time.
    :return: None
    """

    class StubResponse(object):
        """
        Stub response for monkey-patching Http-Request in RssNewsReader
        """
        def __init__(self, content):
            self.status_code = 200
            self.content = content

    def get_stub(*args, **kwargs):
        with open('config/news_rss.xml', 'r', encoding='utf-8') as rss_file:
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
def test_fetch_url_valid():
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



