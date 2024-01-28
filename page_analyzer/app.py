from flask import (Flask,
                   render_template,
                   flash,
                   get_flashed_messages,
                   request,
                   redirect,
                   url_for)

import os
from dotenv import load_dotenv

from page_analyzer.db import (select_all_data_from_urls_by_name,
                              insert_name_into_urls_table,
                              select_id_from_urls_table,
                              select_checks_data,
                              data_from_urls_checks,
                              select_name_and_created_at_from_urls_table,  # noqa 
                              insert_page_data_into_url_checks_table)
from page_analyzer.http import (get_normalized_url,
                                parse_page)

from page_analyzer.validation import url_validate

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    data_for_urls_page = select_checks_data()
    return render_template('urls.html',
                           data_for_urls_page=data_for_urls_page)


@app.post('/urls')
def post_urls():
    entered_url = request.form['url']
    errors = url_validate(entered_url)
    if len(errors) == 0:
        normalized_site_name = get_normalized_url(entered_url)
        data_from_urls = select_all_data_from_urls_by_name(normalized_site_name)  # noqa
        if data_from_urls is None:
            insert_name_into_urls_table(normalized_site_name)
            url_id = select_id_from_urls_table(normalized_site_name)
            flash('Страница успешно добавлена', category='success')
            return redirect(url_for('get_url', id=url_id))
        else:
            url_id = data_from_urls.id
            flash('Страница уже существует', category='info')
            return redirect(url_for('get_url', id=url_id))
    else:
        flash(errors.get('message'), category=errors.get('category'))
        messages = get_flashed_messages(with_categories=True)

        return render_template('index.html', messages=messages), 422


@app.route('/urls/<int:id>')
def get_url(id):
    data_urls_checks = data_from_urls_checks(id)
    name_and_created_at = select_name_and_created_at_from_urls_table(id)
    if name_and_created_at is None:
        return render_template('404.html'), 404
    urls_name = name_and_created_at.name
    urls_created_at = name_and_created_at.created_at
    messages = get_flashed_messages(with_categories=True)
    return render_template('definite_url.html',
                           id=id, name=urls_name,  # noqa
                           urls_created_at=urls_created_at, data_from_urls_checks=data_urls_checks,  # noqa
                           messages=messages)  # noqa


@app.post('/urls/<int:id>/checks')
def run_checks(id):
    name_and_created_at_from_urls = select_name_and_created_at_from_urls_table(id)  # noqa
    if name_and_created_at_from_urls is None:
        return render_template('404.html'), 404
    site_name = name_and_created_at_from_urls.name
    page_data = parse_page(site_name)
    if page_data is None:
        flash('Произошла ошибка при проверке', category='danger')
        return redirect(url_for('get_url', id=id))
    insert_page_data_into_url_checks_table(id, page_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
