FROM python:3.6.7

RUN pip install Flask requests beautifulsoup4

COPY /src /src

CMD ["python3", "/src/proxy.py"]