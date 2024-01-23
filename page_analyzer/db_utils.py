import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception:
        print('Не удалось подключиться к базе данных')


def check_data_availability(normalized_site_name):
    with connect_to_db().cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE name=%s', (normalized_site_name,))  # noqa
        if curs.fetchone() is None:
            return False
        else:
            return True


def insert_name_into_urls_table(name):
    current_date = datetime.now().date().isoformat()
    with connect_to_db() as connect:
        connect.cursor().execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',  # noqa
                                 (name, current_date))

        connect.commit()


def get_id_from_urls_table(site_name):
    with connect_to_db().cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name=%s', (site_name,))
        url_id = curs.fetchone()[0]
        return url_id


def select_data_for_urls_page():
    with connect_to_db().cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT DISTINCT ON (urls.id) urls.id, name, "
                     "COALESCE(CAST(DATE(url_checks.created_at) AS varchar), '') AS created_at, " # noqa
                     "COALESCE(CAST(url_checks.status_code AS varchar), '') AS status_code, " # noqa
                     "COALESCE(CAST(url_checks.id AS varchar), '') AS url_checks_id " # noqa
                     "FROM urls LEFT JOIN url_checks ON urls.id=url_checks.url_id " # noqa
                     "ORDER BY urls.id DESC, url_checks_id DESC") # noqa
        data_for_urls_page = curs.fetchall()
    return data_for_urls_page


def data_from_urls_checks(id):
    id = id
    with connect_to_db().cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * from url_checks where url_id=%s ORDER BY id DESC', (id,)) # noqa
        rows_from_urls_checks = curs.fetchall()
    return rows_from_urls_checks


def select_name_and_created_at_from_urls_table(id):
    id = id
    with connect_to_db().cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls where id=%s ORDER BY id DESC', (id,))
        select_from_urls_table = curs.fetchone()
    return select_from_urls_table


def insert_page_data_into_url_checks_table(id, page_data):
    current_date = datetime.now().date().isoformat()
    with connect_to_db() as connect:
        connect.cursor().execute(
            'INSERT INTO url_checks(url_id, created_at, status_code, title, h1, description) ' # noqa
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (id, current_date, page_data['status_code'], page_data['title'],
             page_data['h1'], page_data['description']))
        connect.commit()
