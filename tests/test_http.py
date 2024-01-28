from page_analyzer.http import *


def test_get_normalized_site_name(get_urls):
    urls = get_urls
    assert get_normalized_url(urls.get('correct')) == 'https://ru.hexlet.io'


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
