# -*- coding: utf-8 -*-

from flask import Flask, request, make_response
from bs4.element import Comment
from bs4 import BeautifulSoup
import requests

import webbrowser
import re

LOCAL_HOST, PORT = '0.0.0.0', 8332
MAIN_HOST = 'https://habr.com'

CHAR_TM = '™'
FREE_TAGS = ('script',)

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    query_string = request.query_string.decode()
    path_with_query_params = '{path}?{qs}'.format(path=path, qs=query_string)

    url = 'https://habr.com/{path}'.format(path=path_with_query_params)
    headers = {
        'User-Agent': request.headers['User-Agent']
    }

    try:
        response = requests.get(url, headers=headers)

    except requests.exceptions.ConnectionError:
        return make_response('<h1>We failed to reach a server.</h1>')

    is_http_request = response.headers['Content-Type'].startswith('text/html')
    content = response.content

    if is_http_request:
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find_all('a', href=re.compile(MAIN_HOST)):
            a['href'] = a['href'].replace(MAIN_HOST, '')

        content_modification(soup.find('body'))

        content = str(soup)

    proxy_response = make_response(content, response.status_code)
    return proxy_response


def content_modification(tag):
    for string in tag.find_all(string=True):
        if string.parent.name in FREE_TAGS or isinstance(string, Comment):
            continue

        text = re.sub(
            r'(?<!\w)(?P<object>\w{6})(?!\w)',
            r'\g<object>{tm}'.format(tm=CHAR_TM),
            str(string)
        )
        string.replace_with(text)


if __name__ == "__main__":
    webbrowser.open('http://{host}:{port}'.format(host=LOCAL_HOST, port=PORT))
    app.run(host=LOCAL_HOST, port=PORT)
