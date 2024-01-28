from validators.url import url
from validators import ValidationError


def url_validate(entered_url):
    errors = {}
    if isinstance(url(entered_url), ValidationError) is True:
        errors['message'] = 'Некорректный URL'
        errors['category'] = 'danger'
        return errors
    else:
        if len(entered_url) > 255:
            errors['message'] = 'URL превышает 255 символов'
            errors['category'] = 'danger'
            return errors
        else:
            return errors
