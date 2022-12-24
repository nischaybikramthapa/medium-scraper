from enum import Enum
from datetime import datetime, timedelta
from typing import List, Union, Tuple, Dict
from bs4.element import Tag
from bs4 import NavigableString
from medium_scraper import settings
import logging
import re

class Period(Enum):
    daily = 1
    weekly = 7
    monthly = 30
    quarterly = 90
    yearly = 365


def construct_start_date(start_date: datetime) -> Tuple[str, str, str]:
    year, month, day = start_date.strftime(settings.DT_FORMAT).split("-")
    return year, month, day


def get_start_date(days: Period) -> datetime:
    return datetime.now() - timedelta(days=days.value)


def init_logger(name: str) -> logging.Logger:
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

def clean_emojis(text: str) -> str:
    """Remove emoji and medium icons from text"""
    text = text.replace("\xa0", " ")
    text = text.replace("\u200a", "")
    text = text.replace("\ufe0f", "")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text


def get_text_from_variants(variants: List[Union[Tag, NavigableString, None]]) -> str:
    """Get text from different variants of elements"""
    found = False
    for variant in variants:
        if ((variant is not None) and (not found)):
            text = variant.text
            text = clean_emojis(text)
            found = True
            return text
    if not found:
        return "NaN"
    return "NaN"

def format_text(text: str) -> str:
    text = text
    text = re.sub(r'\s+[^A-Za-z]', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text

def find_text_from_elements(article_post: Tag, elements: Dict[str, Union[List[str], str]]) -> List[Union[Tag, NavigableString, None]]:
    variants = []
    for element, _classes in elements.items():
        if isinstance(_classes, list):
            for _class in _classes:
                variants.append(article_post.find(element, class_ = _class))
        variants.append(article_post.find(element, class_ = _classes))
    return variants
