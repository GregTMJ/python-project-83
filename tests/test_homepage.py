import re


def test_homepage(client):
    """
    :param client:
    :return:
    """
    response = client.get('/')
    print(response.json)

    assert response.status_code == 200
    assert b"Hello from Greg!" in response.data


def test_urls(client):
    response = client.get('/urls')

    assert response.status_code == 200


def test_post_url(client):
    data = {
        'url': 'https://web.whatsapp.com/'
    }
    response = client.post('/urls',
                           data=data)
    assert response.status_code == 301

    response_data: str = response.get_data().decode('utf-8')
    match = re.findall(r'urls/\d', response_data)[0]
    url_id: int = int(match.split('/')[1])

    response = client.get(f'/urls/{url_id}')
    assert response.status_code == 200
