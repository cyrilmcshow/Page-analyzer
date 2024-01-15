from flask import Flask, render_template, flash, get_flashed_messages, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators.url import url
from validators import ValidationError
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
# namme = 'kek'
# date = datetime.now().date().isoformat()
# print(type(date))
# with conn.cursor() as curs:
#     curs.execute(f'SELECT * FROM urls WHERE name=%s', (namme,))
#     print(curs.fetchone())
# 


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
            current_date = datetime.now().date()
            with conn.cursor() as curs:
                curs.execute(f'SELECT * FROM urls WHERE name=%s', (normalized_site_name, ))
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
            flash('Страница успешно добавлена')


        else:
            flash('Неккоректный URL')
            messages = get_flashed_messages()

            return render_template('index.html', messages=messages)
    else:
        
        with conn.cursor() as curs:
            curs.execute(f'SELECT * FROM urls')
            rows = curs.fetchall()[::-1]
        return render_template('urls.html', rows=rows)

    


@app.route('/urls/<int:id>')
def get_urls_id(id):
    with conn.cursor() as curs:
        curs.execute(f'SELECT * FROM urls where id=%s', (id,))
        row = curs.fetchone()
    messages = get_flashed_messages()
    name = row[1]
    created_at = row[2]
    
    return render_template('definite_url.html', messages=messages, id=id, name=name, created_at=created_at)
