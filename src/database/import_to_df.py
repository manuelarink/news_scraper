from src.database.db_helper import import_data_to_df

DEFAULT_DATABASE_URL = {'database_url': 'postgresql+psycopg2://news:news@localhost:5432/news'}


def import_data():
    '''
    Runs the import of data from database to pandas dataframe.
    :return:
    '''
    df = import_data_to_df(DEFAULT_DATABASE_URL)
    return df


if __name__ == '__main__':
    dataframe = import_data()
