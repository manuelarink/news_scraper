''' Reads all the .csv-Files in data-dir and stores their contents to postgres-database.'''
import sqlalchemy
from sqlalchemy import create_engine
from pathlib import Path
import os
import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)


def connect(**kwargs) -> sqlalchemy.engine.base.Connection:
    '''
    Establishes the db connection.
    :param kwargs:
    :return:
    '''
    engine = create_engine(kwargs['database_url'])
    return engine.connect()


def load_data(csv_file: Path) -> pd.DataFrame:
    '''
    Reads csv-File into Dataframe.
    :param csv_file:
    :return:
    '''
    if csv_file.stat().st_size == 0:
        # ignore empty files
        print(f'{csv_file} empty - skipping')
        return None
    else:
        # read csv into pandas-dataframe
        df = pd.read_csv(csv_file, delimiter=';', quotechar='"', header=None)
        df.columns = ['date', 'title', 'description', 'author',
                      'category', 'copyright', 'url', 'text', 'source']
        return df


def get_dataframe_from_csv_dir(dir_path: Path) -> pd.DataFrame:
    '''
    Reads all csv files and creates one concatenated dataframe with a new column Id
    as primary key.
    '''

    LOGGER.info('enter')

    df_concatenated = pd.DataFrame()

    # iterate over .csv files in data directory, load these to individual dataframe and concatenate to result dataframe
    LOGGER.info(f'check for .csv - files in {dir_path}')
    for csv_file in list(dir_path.rglob('*.csv')):

        LOGGER.info(f'load {csv_file} to dataframe')
        data = load_data(csv_file)

        if data is not None and not data.empty:
            LOGGER.info(f'read {len(data.index)} rows')
            # concatenate the dataframe to the result-dataframe
            df_concatenated = data if df_concatenated.empty else df_concatenated.append(data, ignore_index=True)
        else:
            LOGGER.warning(f'{csv_file} contains no data')

    LOGGER.info(f'created dataframe with {len(df_concatenated.index)} rows')
    return df_concatenated


def replace_and_store(conn: sqlalchemy.engine.base.Connection, dataframe: pd.DataFrame) -> None:
    '''
    Stores data from dataframe to db by replacing the target table 'headlines'.
    :param conn:
    :param dataframe:
    :return:
    '''
    # replace table headlines
    _replace_table(conn.engine)
    # write data to db
    dataframe.to_sql('headlines', con=conn, if_exists='append', index=False)


def disconnect(conn:sqlalchemy.engine.base.Connection) -> None:
    '''
    Disconnects from db.
    :return:
    '''
    conn.close()


def _replace_table(engine: sqlalchemy.engine.Engine) -> None:
    '''
    Replaces the database table for storing the csv-dataframe to.
    :param engine:
    :return:
    '''
    table_name = 'headlines'

    # drop table headlines and index sequence first
    #sql = 'DROP TABLE IF EXISTS headlines; DROP SEQUENCE IF EXISTS headlines_seq'
    sql = 'DROP TABLE IF EXISTS headlines;'
    engine.execute(sql)

    # create new table headlines
    metadata = sqlalchemy.MetaData()
    headlines = sqlalchemy.Table(
        'headlines',
        metadata,
        sqlalchemy.Column(
            'id', sqlalchemy.Integer,
            sqlalchemy.Identity(start=1, cycle=False),
            primary_key=True, unique=True
        ),
        sqlalchemy.Column(
            'date', sqlalchemy.DateTime
        ),
        sqlalchemy.Column(
            'title', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'description', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'author', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'category', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'copyright', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'url', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'text', sqlalchemy.Text
        ),
        sqlalchemy.Column(
            'source', sqlalchemy.Text
        )
    )
    headlines.create(engine)
    # TODO: disconnect... change function parameter to connection instead of engine


def export_csv_to_db(database_url: dict, path: Path) -> None:
    '''
    Exports the data from all .csv-files in data-dir to postgresql-database.
    Replaces the current table headlines by a newly created one.
    :param database_url:
    :param path:
    :return:
    '''
    LOGGER.info('enter')

    # establish connection to db
    conn = connect(**database_url)
    LOGGER.info(f'connection to {database_url} established') if not conn.closed \
        else LOGGER.error(f'connection to {database_url} could not be established')

    # get concatenated dataframe from all .csv in data-dir
    df = get_dataframe_from_csv_dir(path)
    LOGGER.info(f'dataframe with {(len(df.index))} rows to be exported') if not df.empty \
        else LOGGER.warning('empty dataframe')

    # exports the dataframe to db by replacing the old headlines table
    replace_and_store(conn, df)

    # disconnects from db
    disconnect(conn)

    LOGGER.info(f'connection to {database_url} closed') if conn.closed \
        else LOGGER.error(f'connection to {database_url} could not be closed')
    LOGGER.info('exit')


def import_data_to_df(database_url: dict) -> pd.DataFrame:
    '''
    Reads data from postgresql-database into dataframe.
    :param database_url:
    :return:
    '''
    print(os.getcwd())
    conn = connect(**database_url)
    sql = 'SELECT * FROM headlines;'
    df = pd.read_sql(sql, conn)
    print(df)
    disconnect(conn)
    return df

