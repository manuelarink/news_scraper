import requests
from datetime import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
from rssreader import NewsItem


class RSSNewsReader:

    def fetch(self, feed_urls, start_time = None):

        for feed_url in feed_urls:

            print("Lese "+ feed_url["url"] + ":")

            with requests.get(feed_url["url"]) as res:
                doc = BeautifulSoup(res.content, 'lxml')

                items = doc.find_all('item')
                for item in items:

                    # nur aktuelle Einträge (seit letztem Abruf)
                    article_date_str = item.select_one("pubdate").text.strip()
                    article_date = parse(article_date_str)

                    # Veröffentlichungsdatum vergleichen
                    if start_time is not None:
                        if article_date < start_time:
                            # print("Beitrag schon abgerufen")
                            continue

                    news_item = NewsItem()

                    news_item.title = item.select_one("title").text\
                        .replace('<![CDATA[', '')\
                        .replace(']]>', '')\
                        .strip()
                    news_item.url = item.link.next_sibling.replace('\n', '')\
                        .replace('\t', '')\
                        .replace('<![CDATA[', '')\
                        .replace(']]>', '')\
                        .strip()
                    news_item.description = item.select_one("description").text\
                        .replace('<![CDATA[', '')\
                        .replace(']]>', '')\
                        .strip()

                    news_item.date = article_date
                    news_item.source = feed_url["source"]

                    if item.find_all("category"):
                        news_item.category = ', '.join([category.text for category in item.find_all("category")])

                    if item.select_one("author"):
                        news_item.author = item.select_one("author").text

                    if item.select_one("copyright"):
                        news_item.copyright = item.select_one("copyright").text

                    yield news_item

