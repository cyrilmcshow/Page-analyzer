from page_analyzer.validation import validate_url


def test_url_validate(get_urls):
    urls = get_urls

    errors = validate_url(urls.get('correct'))
    assert errors == {}

    errors = validate_url(urls.get('correct2'))
    assert errors == {}

    errors = validate_url(urls.get('incorrect'))
    assert errors['message'] == 'Некорректный URL'
    assert errors['category'] == 'danger'

    errors = validate_url(urls.get('incorrect_len'))
    assert errors['message'] == 'URL превышает 255 символов'
    assert errors['category'] == 'danger'
