from urllib.parse import urlparse
import requests
from requests import RequestException
from bs4 import BeautifulSoup


def get_normalized_url(entered_url):
    parsed_name = urlparse(entered_url)
    normalized_site_name = f'{parsed_name.scheme}://{parsed_name.netloc}'
    return normalized_site_name


def get_response(site_name):
    try:
        response = requests.get(site_name)
        response.raise_for_status()
    except RequestException:
        return
    else:
        return response


def parse_page(response, site_name):
    page_data = {
        'site_name': site_name,
        'status_code': '',
        'h1': '',
        'title': '',
        'description': ''
    }

    soup = BeautifulSoup(response.text, 'html.parser')
    status_code = response.status_code
    h1 = soup.h1
    title = soup.title
    content = soup.find("meta", attrs={'name': 'description'})

    page_data['status_code'] = status_code if status_code else ''
    page_data['h1'] = h1.get_text() if h1 else ''
    page_data['title'] = title.get_text() if title else ''
    page_data['description'] = content["content"] if content else ''

    return page_data
