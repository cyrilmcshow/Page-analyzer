from page_analyzer.app import app
from page_analyzer.db import insert_name_into_urls_table, select_id_from_urls_table, select_all_data_from_urls_by_name
from page_analyzer.http import get_normalized_url
import pytest
from datetime import datetime


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_urls(truncate_db, client):
    response = client.get('/urls')
    assert response.status_code == 200

    text_from_response = response.text
    assert 'Сайты' in text_from_response
    assert 'ID' in text_from_response
    assert 'Имя' in text_from_response
    assert 'Последняя проверка' in text_from_response
    assert 'Код ответа' in text_from_response


def test_get_nonexistent_url(truncate_db, client):
    response = client.get('/urls/100')
    assert response.status_code == 404


def test_add_and_get_existing_url(truncate_db, client, get_urls):
    urls = get_urls
    normalized_url = urls.get('normalized_correct')
    insert_name_into_urls_table(normalized_url)
    data_from_urls_table = select_all_data_from_urls_by_name(normalized_url)

    response = client.get(f'/urls/{data_from_urls_table.id}')
    assert response.status_code == 200

    text_from_response = response.text
    current_date = datetime.now().date().isoformat()
    assert f'{current_date}' in text_from_response
    assert f'Сайт: {data_from_urls_table.name}' in text_from_response
    assert f'{data_from_urls_table.id}' in text_from_response


def test_add_url_post_method(truncate_db, get_urls, client):
    urls = get_urls

    response = client.post('/urls', data={'url': urls.get('correct')})
    assert response.status_code == 302

    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200

    flash = 'Страница успешно добавлена'
    text_from_redirected_response = redirected_response.text
    assert flash in text_from_redirected_response


def test_add_existing_url_post_method(truncate_db, get_urls, client):
    urls = get_urls
    normalized_url = urls.get('normalized_correct')
    insert_name_into_urls_table(normalized_url)

    response = client.post('/urls', data={'url': normalized_url})
    assert response.status_code == 302

    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200

    redirected_response_text = redirected_response.text
    flash = 'Страница уже существует'
    assert flash in redirected_response_text


def test_add_check(truncate_db, get_urls, client):
    urls = get_urls
    normalized_url = urls.get('normalized_correct')
    insert_name_into_urls_table(normalized_url)
    id_from_urls_table = select_id_from_urls_table(normalized_url)

    response = client.post('/urls/' + str(id_from_urls_table) + '/checks', data={'url': normalized_url})
    assert response.status_code == 302

    redirected_response = client.get(response.location, follow_redirects=True)
    assert redirected_response.status_code == 200

    redirected_response_text = redirected_response.text
    flash = 'Страница успешно проверена'
    assert flash in redirected_response_text
