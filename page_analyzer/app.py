from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import psycopg2
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators.url import url
from validators import ValidationError
from datetime import datetime
from bs4 import BeautifulSoup

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    if request.method == 'POST':
        entered_url = request.form['url']
        if isinstance(url(entered_url), ValidationError) is False:
            parsed_name = urlparse(entered_url)
            normalized_site_name = f'{parsed_name.scheme}://{parsed_name.netloc}'
            current_date = datetime.now().date().isoformat()
            with conn.cursor() as curs:
                curs.execute(f'SELECT * FROM urls WHERE name=%s', (normalized_site_name,))
                if curs.fetchone() is None:
                    curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                                 (normalized_site_name, current_date))
                    conn.commit()
                    curs.execute(f'SELECT id FROM urls WHERE name=%s', (normalized_site_name,))
                    id = curs.fetchone()[0]

                    flash('Страница успешно добавлена')
                    return redirect(url_for('get_urls_id', id=id))

                else:
                    curs.execute(f'SELECT id FROM urls WHERE name=%s', (normalized_site_name,))
                    id = curs.fetchone()[0]
                    flash('Страница уже существует')
                    return redirect(url_for('get_urls_id', id=id))



        else:
            if len(url) > 255:
                flash('URL превышает 255 символов')
            else:
                flash('Неккоректный URL')
            messages = get_flashed_messages()

            return render_template('index.html', messages=messages)
    else:
        with conn.cursor() as curs:
            curs.execute(f'SELECT DISTINCT ON (urls.id) urls.id, name, url_checks.created_at, url_checks.status_code, '
                         f'url_checks.id AS url_checks_id FROM urls JOIN url_checks '
                         f'ON urls.id=url_checks.url_id ORDER BY urls.id DESC, url_checks_id DESC')
            rows = curs.fetchall()

        return render_template('urls.html', rows=rows)


@app.route('/urls/<int:id>')
def get_urls_id(id):
    with conn.cursor() as curs:
        curs.execute(f'SELECT * from url_checks where url_id=%s ORDER BY id DESC', (id,))
        rows_from_urls_checks = curs.fetchall()
        if rows_from_urls_checks is None:
            curs.execute(f'SELECT * FROM urls where id=%s ORDER BY id DESC', (id,))
            select_from_urls_table = curs.fetchone()
            messages = get_flashed_messages()
            name = select_from_urls_table[1]
            urls_created_at = select_from_urls_table[2]
            return render_template('definite_url.html', messages=messages, id=id, name=name,
                                   urls_created_at=urls_created_at)

        else:
            curs.execute(f'SELECT * FROM urls where id=%s ORDER BY id DESC', (id,))
            select_from_urls_table = curs.fetchone()
            name = select_from_urls_table[1]
            urls_created_at = select_from_urls_table[2]

            flash('Страница успешно проверена', 'verification')
            messages_about_verification = get_flashed_messages(with_categories=True, category_filter=['verification'])

            return render_template('definite_url.html',
                                   messages_about_verification=messages_about_verification, id=id, name=name,
                                   urls_created_at=urls_created_at, rows=rows_from_urls_checks)


@app.post('/urls/<int:id>/checks')
def run_checks(id):
    current_date = datetime.now().date().isoformat()
    status_code = ''
    title = ''
    h1 = ''
    description_content = ''
    try:
        with conn.cursor() as curs:
            curs.execute(f'SELECT name FROM urls WHERE id=%s', (id,))
            site_name = curs.fetchone()[0]
        r = requests.get(site_name)
        status_code = r.status_code
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')
        try:
            title = soup.title.string
        except Exception:
            print('something wrong')
        try:
            h1 = soup.h1.string
        except Exception:
            print('something wrong')
        try:
            description_content = soup.find('meta', attrs={'name': 'description'})['content']
        except Exception:
            print('something wrong')
    except Exception:
        flash('Произошла ошибка при проверке')
    with conn.cursor() as curs:
        curs.execute(
            f'INSERT INTO url_checks(url_id, created_at, status_code, title, h1, description) VALUES (%s, %s, %s, %s, %s, %s)',
            (id, current_date, status_code, title, h1, description_content))
        conn.commit()

    return redirect(url_for('get_urls_id', id=id))
