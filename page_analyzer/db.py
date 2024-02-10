import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def open_db_connection(func):
    def wrapper(*args, **kwargs):
        connect = connect_to_db()
        with connect:
            with connect.cursor(cursor_factory=NamedTupleCursor) as curs:
                result = func(curs, *args, **kwargs)
                return result

    return wrapper


@open_db_connection
def get_urls_by_name(curs, site_name):
    curs.execute('SELECT * FROM urls WHERE name=%s', (site_name,))  # noqa
    return curs.fetchone()


@open_db_connection
def insert_name_into_urls_table(curs, name):
    current_date = datetime.now().date()
    curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',  # noqa
                 (name, current_date))
    curs.connection.commit()


@open_db_connection
def get_urls_id(curs, site_name):
    curs.execute('SELECT id FROM urls WHERE name=%s', (site_name,))
    url_id = curs.fetchone()[0]
    return url_id


@open_db_connection
def get_checks_data(curs):
    curs.execute("SELECT DISTINCT ON (urls.id) urls.id, name, "
                 "url_checks.created_at AS created_at, "  # noqa
                 "url_checks.status_code AS status_code, "  # noqa
                 "url_checks.id AS url_checks_id "  # noqa
                 "FROM urls LEFT JOIN url_checks ON urls.id=url_checks.url_id "  # noqa
                 "ORDER BY urls.id DESC, url_checks_id DESC")  # noqa
    data_for_urls_page = curs.fetchall()
    return data_for_urls_page


@open_db_connection
def get_checks_data_by_id(curs, id):
    curs.execute('SELECT * from url_checks where url_id=%s ORDER BY id DESC', (id,))  # noqa
    rows_from_urls_checks = curs.fetchall()
    return rows_from_urls_checks


@open_db_connection
def get_name_and_created_at_by_id(curs, id):
    curs.execute('SELECT * FROM urls where id=%s ORDER BY id DESC', (id,))
    select_from_urls_table = curs.fetchone()
    return select_from_urls_table


@open_db_connection
def insert_page_data_into_url_checks_table(curs, id, page_data):
    current_date = datetime.now().date()
    curs.execute(
        'INSERT INTO url_checks(url_id, created_at, status_code, title, h1, description) '  # noqa
        'VALUES (%s, %s, %s, %s, %s, %s)',
        (id, current_date, page_data['status_code'], page_data['title'],
         page_data['h1'], page_data['description']))
    curs.connection.commit()


@open_db_connection
def truncate_db(curs):
    curs.execute('TRUNCATE urls, url_checks CASCADE')
    curs.connection.commit()
