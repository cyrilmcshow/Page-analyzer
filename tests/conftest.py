from pytest import fixture
from page_analyzer.db import truncate_db
from page_analyzer.app import app


@fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@fixture
def get_urls():
    urls = {
        'correct': 'https://ru.hexlet.io/projects/83/members/36239/reviews',
        'normalized_correct': 'https://ru.hexlet.io',
        'correct2': 'https://wrong.name.com',
        'incorrect': 'abcdbhdfdhf',
        'incorrect_len': 'https://ru.hexlet.io/projects/83/members/36239'
                         '/reviews/projects/83/members/36239/reviews/'
                         'projects/83/members/36239/reviews/projects/'
                         '83/members/36239/reviews/projects/83/members/'
                         '36239/reviews/projects/83/members/36239/reviews'
                         '/projects/83/members/36239/reviews/projects/83'
                         '/members/36239/reviews'
    }
    return urls


@fixture
def prepare_db():
    truncate_db()
    yield
