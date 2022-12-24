# Medium article web scraper 

This repository is a python engine that allows you to scrape medium archived articles based on tags. The final output is a CSV file containing the following fields.

```json
{
    "id": "unique_id",
    "title": "title",
    "subtitle": "subtitle",
    "author": "author",
    "publication": "publication",
    "claps": "claps",
    "reading_time": "reading_time",
    "content": "content",
    "link": "article_link",
    "comments": "comments",
    "published_date": "published_date",
    "retrieved_date": "retrieved_date",
        }
```
### Project Structure

```
├── medium_scraper
│   ├── __init__.py
│   ├── article.py
│   ├── commons.py
│   ├── scraper.py
│   └── settings.py
├── Dockerfile
├── main.py
├── pyproject.toml
└── README.md
```
### Prerequisites

- Python 3.8 or above (>= 3.8, < 3.10)
- [poetry](https://python-poetry.org) ([Install guide](https://python-poetry.org/docs/#installation))

### Dependencies
`poetry install`

### Instructions
#### Scraping articles

To retrieve data from medium, simply run `main.py` by passing a tag. The results will be saved in your local directory as `medium_{article_tag}_{date}.csv`

