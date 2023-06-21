import requests
from dateutil.parser import parse
from bs4 import BeautifulSoup
from src.rssreader import NewsItem


class RSSNewsReader:

    def fetch(self, feed_urls, start_time = None):

        for feed_url in feed_urls:

            res = self.request_feed(feed_url)
            doc = self.create_soup(res)

            # find all <item>
            items = doc.find_all('item')
            for item in items:

                # get itemn date
                item_date = self.get_item_date(item)

                # create and yield NewsItem
                if not self.item_already_retrieved(start_time, item_date):
                    news_item = self.create_news_item(item_date, feed_url, item)
                    yield news_item

    @staticmethod
    def item_already_retrieved(start_time, item_date):
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
    def get_item_date(item):
        '''
        Extract the date of the item.
        :param item:
        :return:
        '''
        article_date_str = item.select_one("pubdate").text.strip()
        article_date = parse(article_date_str)
        return article_date

    @staticmethod
    def create_news_item(article_date, feed_url, item):
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

    def create_soup(self, res):
        '''
        Parses the content of rss-feed and creates soup.
        :param res:
        :return:
        '''
        doc = BeautifulSoup(res.content, 'lxml')
        return doc

    def request_feed(self, feed_url):
        '''
        HTTP-Request for retrieving rss-feed from given url.
        :param feed_url:
        :return:
        '''
        print("Lese " + feed_url["url"] + ":")
        res = requests.get(feed_url["url"])
        return res
