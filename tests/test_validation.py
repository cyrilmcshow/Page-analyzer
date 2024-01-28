from page_analyzer.validation import url_validate


def test_url_validate(get_urls):
    urls = get_urls

    errors = url_validate(urls.get('correct'))
    assert errors == {}

    errors = url_validate(urls.get('correct2'))
    assert errors == {}

    errors = url_validate(urls.get('incorrect'))
    assert errors['message'] == 'Некорректный URL'
    assert errors['category'] == 'danger'

    errors = url_validate(urls.get('incorrect_len'))
    assert errors['message'] == 'URL превышает 255 символов'
    assert errors['category'] == 'danger'
