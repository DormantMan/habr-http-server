# -*- coding: utf-8 -*-

from flask import Flask, request, Response
from xml.sax.saxutils import unescape
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
    headers = {key: value for (key, value) in
               filter(lambda header: header[0] != 'Host', request.headers)}

    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True
        )

    except requests.exceptions.ConnectionError:
        return Response('<h1>We failed to reach a server.</h1>')

    is_http_request = response.headers['Content-Type'].startswith('text/html')
    content = response.content

    if is_http_request:
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find_all('a', href=re.compile(MAIN_HOST)):
            a['href'] = a['href'].replace(MAIN_HOST, '')

        for use in soup.find_all('use'):
            use['xlink:href'] = use['xlink:href'].replace(MAIN_HOST, '')

        content_modification(soup.find('body'))

        content = soup.prettify("utf-8")

    excluded_headers = ['content-encoding', 'content-length',
                        'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    proxy_response = Response(content, response.status_code, headers)
    return proxy_response


def content_modification(tag):
    for string in tag.find_all(string=True):
        if string.parent.name in FREE_TAGS or isinstance(string, Comment):
            continue

        text = unescape(string, entities={'&plus': '+'})

        text = re.sub(
            r'(?<!\w)(?P<object>\w{6})(?!\w)',
            r'\g<object>{tm}'.format(tm=CHAR_TM),
            text
        )

        string.replace_with(text)


if __name__ == "__main__":
    webbrowser.open('http://{host}:{port}'.format(host=LOCAL_HOST, port=PORT))
    app.run(host=LOCAL_HOST, port=PORT)
