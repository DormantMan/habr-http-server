from flask import Flask
from flask import request
import webbrowser

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    query_string = request.query_string.decode()
    path_with_query_params = f'{path}?{query_string}'
    return path_with_query_params


if __name__ == "__main__":
    webbrowser.open('http://0.0.0.0:8102')
    app.run(host='0.0.0.0', port=8102)
