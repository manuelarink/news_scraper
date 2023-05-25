import sqlalchemy
from sqlalchemy import create_engine
from pathlib import Path
import os
import pandas as pd

''' Reads all the .csv-Files in data-dir and stores their contents to postgres-database.'''
engine = create_engine("postgresql+psycopg2://news:news@localhost:5432/news")
with engine.connect() as conn:

    # read all csv files and create one concatenated dataframe with a new column Id
    # as primary key;
    # then store this dataframe to db
    df_concatenated = pd.DataFrame()
    path = Path(f'{os.path.dirname(os.path.dirname(__file__))}/data/')
    for csv_file in list(path.rglob('*.csv')):

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

    # define table schema fro dataframe
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
    df_concatenated.to_sql('headlines', con=engine, if_exists='replace', dtype=table_schema, index=True)

    # set primary key
    engine.execute('ALTER TABLE headlines ADD PRIMARY KEY (index);')


