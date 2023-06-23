import datetime
import logging
import bs4.element
import requests
from dateutil.parser import parse
from bs4 import BeautifulSoup
from src.rssreader import NewsItem

LOGGER = logging.getLogger(__name__)


class RSSNewsReader:
    '''
    Class for fetching headlines from rss-News-Feeds and converting them into instances
    of src.rssreader.NewsItem.
    '''

    def fetch(self, feed_urls: list, start_time: datetime.datetime = None) -> NewsItem:
        '''
        Iterates over the list of URLs and requests the contents of the RSS-Feeds,
        parses them and creates instances of class src.rssreader.NewsItem.
        If a start_time is provided only headlines up from this date will be processed.
        :param feed_urls:
        :param start_time:
        :return:
        '''

        for feed_url in feed_urls:

            res = self.request_feed(feed_url)
            doc = self.create_soup(res)

            # find all <item>
            items = doc.find_all('item')
            for item in items:

                # get item date
                item_date = self.get_item_date(item)

                # create and yield NewsItem
                if not self.item_already_retrieved(start_time, item_date):
                    news_item = self.create_news_item(item_date, feed_url, item)
                    yield news_item

    @staticmethod
    def item_already_retrieved(start_time: datetime.datetime, item_date: datetime.datetime) -> bool:
        '''
        Checks if article is older than the ones we want to retrieve.
        :param self:
        :param item_date:
        :param start_time:
        :return:
        '''
        # compare publishing time to start time for retrieving articles
        if start_time is not None:
            return item_date < start_time
        else:
            return False

    @staticmethod
    def get_item_date(item: bs4.element.Tag) -> datetime.datetime:
        '''
        Extract the date of the item.
        :param item:
        :return:
        '''
        article_date_str = item.select_one("pubdate").text.strip()
        article_date = parse(article_date_str)
        return article_date

    @staticmethod
    def create_news_item(article_date: datetime.datetime, feed_url: dict, item: bs4.element.Tag) -> NewsItem:
        '''
        Creates NewsItem from XML-<item>.
        :param article_date:
        :param feed_url:
        :param item:
        :return:
        '''
        news_item = NewsItem()
        news_item.title = item.select_one("title").text \
            .replace('<![CDATA[', '') \
            .replace(']]>', '') \
            .strip()
        news_item.url = item.link.next_sibling.replace('\n', '') \
            .replace('\t', '') \
            .replace('<![CDATA[', '') \
            .replace(']]>', '') \
            .strip()
        news_item.description = item.select_one("description").text \
            .replace('<![CDATA[', '') \
            .replace(']]>', '') \
            .strip()
        news_item.date = article_date
        news_item.source = feed_url["source"]
        if item.find_all("category"):
            news_item.category = ', '.join([category.text for category in item.find_all("category")])
        if item.select_one("author"):
            news_item.author = item.select_one("author").text
        if item.select_one("copyright"):
            news_item.copyright = item.select_one("copyright").text
        return news_item

    @staticmethod
    def create_soup(res: requests.Response):
        '''
        Parses the content of rss-feed and creates soup.
        :param res:
        :return:
        '''
        doc = BeautifulSoup(res.content, 'lxml')
        return doc

    @staticmethod
    def request_feed(feed_url: dict) -> requests.Response:
        '''
        HTTP-Request for retrieving rss-feed from given url.
        If request is not successful returns None
        :param feed_url:
        :return:
        '''
        LOGGER.info('enter')
        LOGGER.info(f'request feed at {feed_url["url"]}')
        res = None
        try:
            res = requests.get(feed_url["url"])
        except ConnectionError as e:
            LOGGER.error(e)
        finally:
            return res
