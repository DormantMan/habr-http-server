#!/usr/bin/env bash

docker build --tag=dormantman-habr-http-proxy .
docker run -it --rm -p 8332:8332 -v $(pwd)/src:/src dormantman-habr-http-proxy