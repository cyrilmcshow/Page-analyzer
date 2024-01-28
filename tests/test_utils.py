import pytest
import psycopg2
from page_analyzer.http import *

URLS = {
    'correct': 'https://ru.hexlet.io/projects/83/members/36239/reviews',
    'correct2': 'https://wrong.name.com',
    'incorrect': 'abcdbhdfdhf',
    'incorrect2': 'google.com'
}


def test_url_validate():
    assert url_validate(URLS.get('correct'))
    assert url_validate(URLS.get('correct2'))
    assert not url_validate(URLS.get('incorrect'))
    assert not url_validate(URLS.get('incorrect2'))


def test_get_normalized_site_name():
    assert get_normalized_url(URLS.get('correct')) == 'https://ru.hexlet.io'


def test_page_parse():
    expected_data = {
        'site_name': 'https://ru.hexlet.io',
        'status_code': 200,
        'h1': 'Лучшая школа программирования по\xa0версии пользователей Хабра',
        'title': 'Хекслет — онлайн-школа программирования, онлайн-обучение ИТ-профессиям',
        'description': 'Хекслет — лучшая школа программирования по версии пользователей Хабра. Авторские программы '
                       'обучения с практикой и готовыми проектами в резюме. Помощь в трудоустройстве после успешного '
                       'окончания обучения'
    }
    assert parse_page('https://ru.hexlet.io') == expected_data
