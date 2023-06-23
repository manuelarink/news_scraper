import pytest
from src.rssreader import NewsItem
from copy import deepcopy


#@pytest.mark.skip('Skipped for no reason')
#@pytest.mark.skipif(pytest.__version__ < '5.5.0', reason='just as example for conditional skipping')
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
    news_item = NewsItem(date, description, url, author, title, text, category, copyright, source)
    assert news_item.date == date
    assert news_item.description == description
    assert news_item.url == url
    assert news_item.author == author
    assert news_item.title == title
    assert news_item.text == text
    assert news_item.category == category
    assert news_item.copyright == copyright
    assert news_item.source == source


@pytest.mark.newsItem
def test_items_should_be_equal(input_news_item):
    """
    test of correct implementation of NewsItem.__eq__ function
    """
    news_item1 = input_news_item
    news_item2 = deepcopy(input_news_item)

    assert news_item1 == news_item2


@pytest.mark.newsItem
@pytest.mark.parametrize('date, description, url, author, title, text, category, copyright, source, expected_result',
                         [('2022-07-04 13:27:38',
                           'Test Description',
                           'https://test.de/rss',
                           'Test Author',
                           'Test Title',
                           'Test Text',
                           'Test Category',
                           'Test Copyright',
                           'Test Source',
                           'Date=2022-07-04 13:27:38, Description=Test Description, '
                           'URL=https://test.de/rss, Author=Test Author, '
                           'Title=Test Title, Text=Test Text, '
                           'Category=Test Category, Copyright=Test Copyright, Source=Test Source'),
                          ('', '', '', '', '', '', '', '', '', 'Date=, Description=, URL=, Author=, '
                                                               'Title=, Text=, Category=, Copyright=, Source=')])
def test_str(date, description, url, author, title, text, category, copyright, source, expected_result):
    """
    Test on correct implementation of __str__ method.
    :return:
    """
    news_item = NewsItem(date, description, url, author, title, text, category, copyright, source)
    assert str(news_item) == expected_result
