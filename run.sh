#!/usr/bin/env bash

docker build --tag=dormantman-habr-proxy .
docker run -it --rm -p 8102:8102 -v $(pwd)/src:/src dormantman-habr-proxy