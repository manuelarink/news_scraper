import pytest
from rssreader import NewsItem
import sys
from copy import deepcopy
from dateutil.parser import parse

#@pytest.mark.skip('Skipped for no reason')
#@pytest.mark.skipif(pytest.__version__ < '5.5.0', reason='just as example for contiional skipping')
@pytest.mark.newsItem
@pytest.mark.parametrize('date, description, url, author, title, text, category, copyright, source',
                         [('2022-07-04 13:27:38',
                           'Nach 12 Jahren erscheinen die ZDF-Nachrichten im neuen Look. '
                           'Werfen Sie einen Blick hinter die Kulissen – und entdecken das '
                           'neue Studio in unserer 3D-Story.',
                           'https://3d.zdf.de/nachrichten-studio-design/',
                           'Test Author',
                           'Entdecken Sie das ZDF-Nachrichtenstudio',
                           'Test Text',
                           '3D-Modell',
                           'Copyright: Test Author',
                           'ZDF heute'),
                          ('', '', '', '', '', '', '', '', '')])
def test_should_init_news_item_with_attrs(date, description, url, author, title, text, category, copyright, source):
    """
    test of correct initialising of NewsItem-instance with given attrs
    """
    newsItem = NewsItem(date, description, url, author, title, text, category, copyright, source)
    assert newsItem.date == date
    assert newsItem.description == description
    assert newsItem.url == url
    assert newsItem.author == author
    assert newsItem.title == title
    assert newsItem.text == text
    assert newsItem.category == category
    assert newsItem.copyright == copyright
    assert newsItem.source == source

@pytest.mark.newsItem
def test_items_should_be_equal(input_news_item):
    """
    test of correct implementation of NewsItem.__eq__ function
    """
    newsItem1 = input_news_item
    newsItem2 = deepcopy(input_news_item)

    assert newsItem1 == newsItem2
