# habr-http-server
Simple http proxy server

### Run
You can run through run.sh
```sh
./run.sh
```
or via python
```sh
pip install Flask requests beautifulsoup4
python3 ./src/proxy.py
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
python -m webbrowser "http://localhost:8332"
```

### Docker
Simply use the Dockerfile to build the image

```sh
docker build --tag=dormantman-habr-http-proxy .
docker run -it --rm -p 8332:8332 -v $(pwd)/src:/src dormantman-habr-http-proxy
```
