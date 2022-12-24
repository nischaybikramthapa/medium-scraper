from bs4.element import Tag
from typing import Union, Dict, Any
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import uuid
from medium_scraper import commons
from medium_scraper import settings


class ArticleParser:
    def __init__(self, frequency: commons.Period) -> None:
        self.frequency = frequency

    def _get_title(self, article_post: Tag) -> str:
        variants = commons.find_text_from_elements(
            article_post, settings.TITLE_ELEMENTS
        )
        title = commons.get_text_from_variants(variants)
        return title

    def _get_subtitle(self, article_post: Tag) -> str:
        variants = commons.find_text_from_elements(
            article_post, settings.SUBTITLE_ELEMENTS
        )
        subtitle = commons.get_text_from_variants(variants)
        return subtitle

    def _get_author(self, article_post: Tag) -> str:
        author = article_post.find(
            "a",
            class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken",
        )
        if author is not None:
            return commons.format_text(author.text)
        return "NaN"

    def _get_publication(self, article_post: Tag) -> str:
        pub = article_post.find(
            "a",
            class_="ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal",
        )
        if pub is not None:
            return commons.format_text(pub.text)
        return "NaN"

    def _get_read_time(self, article_post: Tag) -> str:
        reading_time = article_post.find("span", class_="readingTime")
        if reading_time is not None:
            reading_time = reading_time["title"]  # type: ignore
            reading_time = reading_time.replace(" min read", "")  # type: ignore
        return "0"

    def _get_claps(self, article_post: Tag) -> str:
        claps = article_post.find(
            "button",
            class_="button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents",
        )
        if claps is not None:
            return claps.text
        return "0"

    def _get_comments(self, article_post: Tag) -> int:
        comment = article_post.find(
            "div",
            class_="u-fontSize14 u-marginTop10 u-marginBottom20 u-padding14 u-xs-padding12 u-borderRadius3 u-borderCardBackground u-borderLighterHover u-boxShadow1px4pxCardBorder",
        )
        if comment is not None:
            return 1
        return 0

    def _get_article_link(self, article_post: Tag) -> Union[str, None]:
        url = article_post.find("a", class_="")
        if url is not None:
            return url["href"]  # type: ignore
        raise Exception("Couldnt find a url")

    def _get_content(self, post_url: str) -> str:
        try:
            article = requests.get(post_url)
            article_soup = BeautifulSoup(article.text, "html.parser")
            sections = article_soup.find_all("section")
            contents = []
            for section in sections:
                paragraphs = section.find_all("p")
                for paragraph in paragraphs:
                    contents.append(paragraph.text)
            full_content = " ".join(contents)
            return full_content
        except:
            raise Exception(f"Fail to fetch from {post_url}")

    def parse(self, article_post: Tag) -> Dict[str, Any]:
        link = self._get_article_link(article_post)
        content = self._get_content(link)  # type: ignore
        title = self._get_title(article_post)
        subtitle = self._get_subtitle(article_post)
        author = self._get_author(article_post)
        publication = self._get_publication(article_post)
        reading_time = self._get_read_time(article_post)
        comments = self._get_comments(article_post)
        claps = self._get_claps(article_post)
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "publication": publication,
            "claps": claps,
            "reading_time": reading_time,
            "content": content,
            "link": link,
            "comments": comments,
            "published_date": commons.get_start_date(self.frequency),
            "retreived_date": datetime.today().date(),
        }
