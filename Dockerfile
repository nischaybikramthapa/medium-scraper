FROM --platform=linux/amd64 python:3.8

COPY . /tmp/scraper/
WORKDIR /tmp/scraper
RUN pip install poetry
RUN poetry install

CMD ["python3", "main.py"]