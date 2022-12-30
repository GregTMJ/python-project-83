from bs4 import BeautifulSoup


def page_parser(content):
    """
    Getting the main content from page content (title, h1, description)
    :param content: GET page content
    :return: dict()
    """
    soup = BeautifulSoup(content, 'html.parser')
    title: str = soup.find('title').text if soup.find('title') else ''
    h1: str = soup.find('h1').text if soup.find('h1') else ''
    description: str = ''
    description_meta = soup.find('meta', attrs={'name': 'description'})

    if description_meta:
        description = description_meta['content']

    return {
        'title': title,
        'h1': h1,
        'description': description
    }
