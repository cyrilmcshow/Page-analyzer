from pytest import fixture
from page_analyzer.db import clear_db


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
def truncate_db():
    yield
    clear_db()