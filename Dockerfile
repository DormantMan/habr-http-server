FROM python:3.6.3

RUN pip install Flask

COPY /src /src

CMD ["python3", "/src/proxy.py"]