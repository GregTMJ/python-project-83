import validators

from urllib.parse import urlparse


def url_normalizer(start_url: str) -> str:
    """
    Sometimes we are given not a correct interpreted URL, for that
    reason, we should make it more obvious to Python to interact
    with
    :return: normalized https:// + URL
    """
    normalized_url = urlparse(start_url)
    return f'{normalized_url.scheme}://{normalized_url.netloc}'


def validate(start_url: str) -> list[str]:
    """
    Everytime we get a unique URL from user, we should check if
    it's valid to add/use
    :return: errors if triggered
    """
    errors: list[str] = []
    if len(start_url) > 255:
        errors.append('URL превышает 255 символов')
    if not validators.url(start_url):
        errors.append('Некорректный URL')
    if not start_url:
        errors.append('URL обязателен')
    return errors
