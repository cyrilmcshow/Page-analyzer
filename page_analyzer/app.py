from flask import (Flask,
                   render_template,
                   flash,
                   get_flashed_messages,
                   request,
                   redirect,
                   url_for)

import os
from dotenv import load_dotenv

from page_analyzer.db_utils import (check_data_availability,
                                    insert_name_into_urls_table,
                                    get_id_from_urls_table,
                                    select_data_for_urls_page,
                                    data_from_urls_checks,
                                    select_name_and_created_at_from_urls_table,  # noqa 
                                    insert_page_data_into_url_checks_table)
from page_analyzer.utils import (url_validate,
                                 get_normalized_site_name,
                                 parse_page)

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    if request.method == 'POST':
        entered_url = request.form['url']
        if url_validate(entered_url):
            normalized_site_name = get_normalized_site_name(entered_url)
            if check_data_availability(normalized_site_name) is False:
                insert_name_into_urls_table(normalized_site_name)
                url_id = get_id_from_urls_table(normalized_site_name)
                flash('Страница успешно добавлена', category='success')
                return redirect(url_for('get_definite_url', id=url_id))
            else:
                url_id = get_id_from_urls_table(normalized_site_name)
                flash('Страница уже существует', category='info')
                return redirect(url_for('get_definite_url', id=url_id))
        else:
            if len(entered_url) > 255:
                flash('URL превышает 255 символов', category='danger')
            else:
                flash('Некорректный URL', category='danger')
            messages = get_flashed_messages(with_categories=True)

            return render_template('index.html', messages=messages), 422
    else:
        data_for_urls_page = select_data_for_urls_page()
        return render_template('urls.html',
                               data_for_urls_page=data_for_urls_page)


@app.route('/urls/<int:id>')
def get_definite_url(id):
    data_urls_checks = data_from_urls_checks(id)
    if not data_urls_checks:
        name_and_created_at = select_name_and_created_at_from_urls_table(id)
        urls_name = name_and_created_at.name
        urls_created_at = name_and_created_at.created_at
        messages = get_flashed_messages(with_categories=True)
        return render_template('definite_url.html',
                               messages=messages, id=id, name=urls_name,
                               urls_created_at=urls_created_at)

    else:
        name_and_created_at = select_name_and_created_at_from_urls_table(id)
        urls_name = name_and_created_at.name
        urls_created_at = name_and_created_at.created_at
        messages = get_flashed_messages(with_categories=True)

        return render_template('definite_url.html',
                            id=id, name=urls_name, # noqa
                            urls_created_at=urls_created_at, data_from_urls_checks=data_urls_checks, # noqa
                            messages=messages) # noqa


@app.post('/urls/<int:id>/checks')
def run_checks(id):
    site_name = select_name_and_created_at_from_urls_table(id).name
    page_data = parse_page(site_name)
    if page_data is None:
        flash('Произошла ошибка при проверке', category='danger')
        return redirect(url_for('get_definite_url', id=id))
    insert_page_data_into_url_checks_table(id, page_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_definite_url', id=id))
