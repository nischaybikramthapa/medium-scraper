from datetime import datetime, timedelta
from bs4 import BeautifulSoup, ResultSet
from medium_scraper.driver import WebDriver
from medium_scraper.commons import *
from typing import List, Dict
from medium_scraper.article import ArticleParser
from medium_scraper import settings
import requests
import pandas as pd
import time


class MediumScraper:
    def __init__(self, article_tag: str, frequency: str = "daily") -> None:
        self.logger = init_logger(self.__class__.__name__)
        self.article_tag = article_tag
        self.frequency = getattr(Period, frequency)
        self.base_url = "https://medium.com/tag"
        self.end_date = datetime.today()

    def _create_url(self, start_date: datetime = None) -> str:
        year, month, day = construct_start_date(start_date)
        return f"{self.base_url}/{self.article_tag}/archive/{year}/{month}/{day}"

    def _get_articles(self, soup: BeautifulSoup) -> ResultSet:
        """Pulls each card from the feed. Each card is either a story or a comment"""
        self.logger.info("Fetching all articles from the top element")
        article_posts = soup.find_all(
            "div", class_="streamItem streamItem--postPreview js-streamItem"
        )
        return article_posts

    def _convert_to_df(self, records: List[Dict[str, str]]) -> pd.DataFrame:
        """Converts list of dictionary into a data frame"""
        return pd.DataFrame(records)

    def _save_to_file(self, data: List[pd.DataFrame]) -> None:
        """Concats data from all dates and save a file as a csv"""
        df = pd.concat(data, axis=0)
        self.logger.info(f"Retrieved {df.shape[0]} articles from {self.article_tag}")
        date_stamp = self.end_date.astimezone(settings.LOCAL_TZ).strftime(
            settings.DT_FORMAT
        )
        self.logger.info(
            f"Saving dataframe to medium_{self.article_tag}_{date_stamp}.csv"
        )
        df.to_csv(f"medium_{self.article_tag}_{date_stamp}.csv", index=False)

    def scrape_from_tags(self):
        start_date = get_start_date(self.frequency)
        all_articles = []
        while start_date <= self.end_date:
            self.logger.info(f"Scraping {self.base_url} for {start_date} ")
            url = self._create_url(start_date)
            self.logger.info(f"Fetching contents from {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, features="lxml")
            articles = self._get_articles(soup)
            records = [
                ArticleParser(self.frequency).parse(article) for article in articles
            ]
            all_articles.append(self._convert_to_df(records))
            start_date = start_date + timedelta(days=1)  # fetch for the next day
            time.sleep(5)  # Take some rest
        self._save_to_file(all_articles)
