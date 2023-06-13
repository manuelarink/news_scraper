import csv
import pytz
import os
from datetime import datetime
from src.rssreader import RSSNewsReader


class NewsScraper:

    def __init__(self, feed_urls):
        self.feed_urls = feed_urls

    def scrape(self):
        # aktuelles Datum ermitteln - Nachrichten eines Tages werden in je einem File gespeichert
        tz_berlin = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz_berlin)
        str_now = now.strftime("%Y-%m-%d_%H-%M-%S")
        ctrl_file = os.path.join(os.path.dirname(__file__), '../data', '.rss_news_reader')
        news_file_name = 'news-' + str_now + '.csv'
        news_file = os.path.join(os.path.dirname(__file__), '../data', news_file_name)

        # Ctrl-File öffnen und letzten Abruf (= Eintrag) ermitteln
        with open(ctrl_file, 'r') as ctrlfile:
            ctrl_csvreader = csv.reader(ctrlfile)
            last_update = next(ctrl_csvreader)[0]
            print(last_update)

        with open(news_file, 'a', newline='', encoding='utf-8') as csvfile:
            news_reader = RSSNewsReader()
            for news_item in news_reader.fetch(self.feed_urls, datetime.fromisoformat(last_update)):
                print(str(news_item.date) + ":: Titel: " + news_item.title + ", Beschreibung: " + news_item.description)

                csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
                csvwriter.writerow([
                    str(news_item.date),
                    news_item.title,
                    news_item.description,
                    news_item.author,
                    news_item.category,
                    news_item.copyright,
                    news_item.url,
                    news_item.text,
                    news_item.source])

        with open(ctrl_file, 'w', newline='', encoding='utf-8') as ctrlfile:
            ctrl_csvwriter = csv.writer(ctrlfile, delimiter=';', quotechar="'")
            ctrl_csvwriter.writerow([now])

if __name__ == '__main__':

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

    scraper = NewsScraper(sources)
    scraper.scrape()
