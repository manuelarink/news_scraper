import pytest
from database import db_store
from sqlalchemy.exc import SQLAlchemyError

mock_db_url = {'database_url':
                   'sqlite+pysqlite:///:memory:'}

@pytest.mark.db_store
def test_connect_to_db_success(setup_db_with_mock):
    '''
    Test on successful connecting to db.
    :param setup_db_with_mock:
    :return:
    '''
    assert setup_db_with_mock is not None

@pytest.mark.db_store
@pytest.mark.parametrize('database_url',
                         ['unknown_dialect+psycopg2://news:news@localhost:5432/news',
                          'postgresql+unknown_dbapi://news:news@localhost:5432/news',
                          'postgresql+psycopg2://unknown_user:news@localhost:5432/news',
                          'postgresql+psycopg2://news:unknown_pwd@localhost:5432/news',
                          'postgresql+psycopg2://news:news@unknown_host:5432/news]',
                          #'postgresql+psycopg2://news:news@localhost:0/news',
                          'postgresql+psycopg2://news:news@localhost:5432/unknown_db'])
def test_connect_to_db_fails(database_url):
    '''
    Test on failure establishing connection.
    :param database_url:
    :return:
    '''
    with pytest.raises(SQLAlchemyError):
        con = db_store.connect(**{'database_url': database_url})

@pytest.mark.db_store
def test_disconnect_successful(setup_db_with_mock):
    '''
    Test on successful close of db-connection.
    '''
    con = db_store.connect(**mock_db_url)
    db_store.disconnect(con)
    assert con.closed is True
