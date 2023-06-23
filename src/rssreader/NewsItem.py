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

    def __repr__(self):
        return (f'Date={self.date!r}, Description={self.description!r}, '
                f'URL={self.url!r}, Author={self.author!r}, '
                f'Title={self.title!r}, Text={self.text!r}, '
                f'Category={self.category!r}, Copyright={self.copyright!r}, '
                f'Source={self.source!r}')

    def __str__(self):
        return (f'Date={self.date}, Description={self.description}, '
                f'URL={self.url}, Author={self.author}, '
                f'Title={self.title}, Text={self.text}, '
                f'Category={self.category}, Copyright={self.copyright}, '
                f'Source={self.source}')

