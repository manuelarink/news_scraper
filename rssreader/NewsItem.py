class NewsItem:

    def __init__(self, date="",
                 description="",
                 url="",
                 author="",
                 title="",
                 text="",
                 category="",
                 copyright="",
                 source=""):
        self.date = date
        self.description = description
        self.url = url
        self.author = author
        self.title = title
        self.text = text
        self.category = category
        self.copyright = copyright
        self.source = source

    def __eq__(self, other):
        return self.date == other.date \
               and self.description == other.description \
               and self.url == other.url \
               and self.author == other.author \
               and self.title == other.title \
               and self.text == other.text \
               and self.category == other.category \
               and self.copyright == other.copyright \
               and self.source == other.source

    def __str__(self):
        return f'Date={self.date}\n Description={self.description}\n ' \
               f'URL={self.url}\n Author={self.author}\n ' \
               f'Title={self.title}\n Text={self.text}\n' \
               f'Category={self.category}\n Copyright={self.copyright}\n' \
               f'Source={self.source}'

