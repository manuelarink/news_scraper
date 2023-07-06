import csv
import logging
import pytz
import datetime
import src.database.db_helper as db_helper
from pathlib import Path
from src.rssreader import RSSNewsReader

LOGGER = logging.getLogger(__name__)
# TODO store database url in config file
DEFAULT_DATABASE_URL = {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}


class NewsScraper:
    '''Scrapes news from RSS feeds and stores them in a csv file.
    The csv file is stored in the data folder.
    The file name is news-<date>.csv
    The file contains the following columns:
    - date
    - title
    - description
    - author
    - category
    - copyright
    - url
    - text
    - source
    '''

    SOURCES = [
        {"source": "Focus", "url": "https://rss.focus.de/politik/"},
        {"source": "Focus", "url": "https://rss.focus.de/politik/ausland/"},
        {"source": "stern", "url": "https://www.stern.de/feed/standard/politik"},
        {"source": "Tagesschau", "url": "https://www.tagesschau.de/xml/rss2/"},
        {"source": "Welt", "url": "https://www.welt.de/feeds/topnews.rss"},
        {"source": "Zeit", "url": "https://newsfeed.zeit.de/index"},
        {"source": "taz", "url": "https://taz.de/!p4608;rss/"},
        {"source": "ZDF heute", "url": "https://www.zdf.de/rss/zdf/nachrichten"}
    ]

    def __init__(self, feed_urls):
        '''Initializes the NewsScraper with a list of feed urls.
        :param feed_urls: list of feed urls
        '''
        LOGGER.info('Initializing NewsScraper')
        self.feed_urls = feed_urls

    def scrape(self) -> Path:
        '''Scrapes the news from the feed urls and stores them in a csv file.
        The csv file is stored in the data folder.
        The file name is news-<date>.csv
        The file contains the following columns:
        - date
        - title
        - description
        - author
        - category
        - copyright
        - url
        - text
        - source
        :return: the news file path
        :rtype: Path
        '''
        LOGGER.info('Scraping news')

        # get current date and time
        str_now, tz_berlin = self.get_local_datetime()

        # get base dir of news file
        base_dir = Path(__file__).resolve().parent.parent
        LOGGER.debug(f'Base dir: {base_dir}')

        # build ctrl file path
        ctrl_file = self.build_ctrl_file_path(base_dir)

        # build news file path
        news_file = self.build_news_file_path(base_dir, str_now)

        # open ctrl file and read last update
        last_update = self.read_last_update(ctrl_file)

        with open(news_file, 'a', newline='', encoding='utf-8') as csvfile:
            print(type(csvfile))
            news_reader = RSSNewsReader()
            self.write_news_to_csv(csvfile, last_update, news_reader)

        self.write_last_update(ctrl_file, datetime.datetime.now(tz_berlin).isoformat())

        LOGGER.info('Scraping news finished')
        return news_file

    def get_local_datetime(self) -> (str, pytz.timezone):
        '''
        Returns the current date and time in the timezone Europe/Berlin.
        :return: current date and time, timezone
        :rtype: str, pytz.timezone
        '''
        LOGGER.debug('Getting local date and time')
        tz_berlin = pytz.timezone('Europe/Berlin')
        now = datetime.datetime.now(tz_berlin)
        str_now = now.strftime("%Y-%m-%d_%H-%M-%S")
        LOGGER.debug(f'Local date and time: {str_now}')
        return str_now, tz_berlin

    def build_news_file_path(self, base_dir: Path, str_now: str) -> Path:
        '''
        Builds the news file path.
        :param base_dir: base dir
        :type base_dir: Path
        :param str_now: the current date and time
        :type str_now: str
        :return: news file path
        :rtype: Path
        '''
        LOGGER.debug('Building news file path')
        news_file_name = f'news-{str_now}.csv'
        news_file = base_dir / 'data' / news_file_name
        LOGGER.debug(f'News file: {news_file}')
        return news_file

    def build_ctrl_file_path(self, base_dir: Path) -> Path:
        '''
        Builds the control file path.
        :param base_dir: base dir
        :type base_dir: Path
        :return: ctrl file path
        :rtype: Path
        '''
        LOGGER.debug('Building ctrl file path')
        ctrl_file = base_dir / 'data' / '.rss_news_reader'
        LOGGER.debug(f'Control file: {ctrl_file}')
        return ctrl_file

    def write_news_to_csv(self, csvfile, last_update: str, news_reader: RSSNewsReader) -> None:
        '''
        Writes the news to the csv file.
        :param csvfile: csv file
        :type csvfile: TextIOWrapper
        :param last_update: timestamp of the last update, up from this point the news are fetched
        :type last_update: str
        :param news_reader: RSSNewsReader
        :type news_reader: RSSNewsReader
        :return: None
        :rtype: None
        '''
        for news_item in news_reader.fetch(self.feed_urls, datetime.datetime.fromisoformat(last_update)):
            LOGGER.info(f'Writing news item: {news_item}')
            print(f'{news_item.date}:: Titel: {news_item.title}, Beschreibung: {news_item.description}')

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
            LOGGER.info(f'News item written')

    def write_last_update(self, ctrl_file: Path, timestamp: str) -> None:
        '''
        Writes the timestamp of the last update to the control file.
        :param ctrl_file:  control file name
        :type ctrl_file: Path
        :param timestamp:   timestamp of the last update
        :type timestamp: str
        :return:    None
        '''
        LOGGER.info(f'Writing last update to {ctrl_file}')
        with open(ctrl_file, 'w', newline='', encoding='utf-8') as ctrlfile:
            ctrl_csvwriter = csv.writer(ctrlfile, delimiter=';', quotechar="'")

            ctrl_csvwriter.writerow([timestamp])
            LOGGER.info(f'last updated on: {timestamp}')

    def read_last_update(self, ctrl_file: Path) -> str:
        '''
        Reads the timestamp of the last update from the control file. If the file does not exist, the current timestamp is returned.
        :param ctrl_file: control file name
        :type ctrl_file: str
        :return:    timestamp of the last update
        :rtype: str
        '''
        LOGGER.info(f'Reading last update from {ctrl_file}')
        with open(ctrl_file, 'r') as ctrlfile:
            ctrl_csvreader = csv.reader(ctrlfile)
            last_update = next(ctrl_csvreader)[0]
        LOGGER.info(f'last updated on: {last_update}')
        return last_update

    def write_csv_to_db(self, csvfile_path: Path, db_url: dict) -> None:
        '''
        Appends the rows of the csv file to the database table.
        :param csvfile_path: csv file path
        :type csvfile_path: Path
        :param db_url: database url
        :type db_url: dict
        :return: None
        :rtype: None
        '''
        LOGGER.info(f'Exporting csv file {csvfile_path} to db')
        db_helper.insert_csv_to_db(db_url, csvfile_path)
        LOGGER.info(f'Exporting csv file {csvfile_path} to db finished')


if __name__ == '__main__':
    LOGGER.info('Starting NewsScraper')
    scraper = NewsScraper(NewsScraper.SOURCES)
    result = scraper.scrape()
    scraper.write_csv_to_db(result, DEFAULT_DATABASE_URL)
    LOGGER.info('Finished NewsScraper')

