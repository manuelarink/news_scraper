''' Reads all the .csv-Files in data-dir and stores their contents to postgres-database.'''
import sqlalchemy
from sqlalchemy import create_engine
from pathlib import Path
import os
import pandas as pd


def connect(**kwargs) -> sqlalchemy.engine.mock.MockConnection:
    '''
    Establishes the db connection.
    :param kwargs:
    :return:
    '''
    engine = create_engine("postgresql+psycopg2://news:news@localhost:5432/news")
    return engine.connect()


def get_dataframe_from_csv(dir_path: Path) -> pd.DataFrame:
    '''
    Reads all csv files and creates one concatenated dataframe with a new column Id
    as primary key.
    '''

    df_concatenated = pd.DataFrame()
    for csv_file in list(dir_path.rglob('*.csv')):

        if csv_file.stat().st_size == 0:
            print(f'{csv_file} empty - skipping')
            continue

        # read csv into pandas-dataframe
        df = pd.read_csv(csv_file, delimiter=';', quotechar='"', header=None)
        df.columns = ['Date', 'Title', 'Description', 'Author',
                      'Category', 'Copyright', 'Url', 'Text', 'Source']

        # remove whites spaces, '\n', '\t', '\r' from text cells
        # df[['Date', 'Title', 'Description',
        #     'Author', 'Category',
        #     'Url', 'Source']].apply(lambda x: x.str.strip())

        # concatenate the dataframe to the result-dataframe
        df_concatenated = df if df_concatenated.empty else df_concatenated.append(df, ignore_index=True)

    # add a new column for the serial number
    #df_concatenated['Id'] = range(1, len(df_concatenated) + 1)
    print(df_concatenated)
    return df_concatenated


def store_to_db(conn: sqlalchemy.engine.mock.MockConnection, dataframe: pd.DataFrame) -> None:
    '''
    Stores data from dataframe to db by replacing the target table 'headlines'.
    :param conn:
    :param dataframe:
    :return:
    '''
    # define table schema for dataframe
    table_schema = {'Date': sqlalchemy.DateTime,
                    'Title': sqlalchemy.String,
                    'Description': sqlalchemy.String,
                    'Author': sqlalchemy.String,
                    'Category': sqlalchemy.String,
                    'Copyright': sqlalchemy.String,
                    'Url': sqlalchemy.String,
                    'Text': sqlalchemy.String,
                    'Source': sqlalchemy.String}
                    #'Id': sqlalchemy.BigInteger}

    # write data to db
    dataframe.to_sql('headlines', con=conn, if_exists='replace', dtype=table_schema, index=True)

    # set primary key
    conn.execute('ALTER TABLE headlines ADD PRIMARY KEY (index);')


if __name__ == '__main__':
    conn = connect()
    path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/data/')
    df = get_dataframe_from_csv(path)
    store_to_db(conn, df)
