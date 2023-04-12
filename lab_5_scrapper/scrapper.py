"""
Crawler implementation
"""
import datetime
import json
import re
import shutil
from pathlib import Path
from typing import Pattern, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from core_utils.article.article import Article
# from core_utils.article.io import to_meta, to_raw
from core_utils.config_dto import ConfigDTO
from core_utils.constants import (ASSETS_PATH, CRAWLER_CONFIG_PATH,
                                  NUM_ARTICLES_UPPER_LIMIT,
                                  TIMEOUT_LOWER_LIMIT, TIMEOUT_UPPER_LIMIT)

class IncorrectSeedURLError(Exception):
    """
    Validates a seed url format
    """


class NumberOfArticlesOutOfRangeError(Exception):
    """
    Validates the number of articles within the necessary range
    """


class IncorrectNumberOfArticlesError(Exception):
    """
    Validates the type of number of articles
    """


class IncorrectHeadersError(Exception):
    """
    Validates the type of header
    """


class IncorrectEncodingError(Exception):
    """
    Validates the type of encoding
    """


class IncorrectTimeoutError(Exception):
    """
    Validates timeout
    """


class IncorrectVerifyError(Exception):
    """
    Validates the verify attribute
    """

class Config:
    """
    Unpacks and validates configurations
    """
    seed_urls: list[str]
    total_articles_to_find_and_parse: int
    headers: dict[str, str]
    encoding: str
    timeout: int
    verify_certificate: bool
    headless_mode: bool

    def __init__(self, path_to_config: Path) -> None:
        """
        Initializes an instance of the Config class
        """
        self.path_to_config = path_to_config
        self._validate_config_content()
        config_dto = self._extract_config_content()
        self._seed_urls = config_dto.seed_urls
        self._num_articles = config_dto.total_articles
        self._headers = config_dto.headers
        self._encoding = config_dto.encoding
        self._timeout = config_dto.timeout
        self._should_verify_certificate = config_dto.should_verify_certificate
        self._headless_mode = config_dto.headless_mode

    def _extract_config_content(self) -> ConfigDTO:
        """
        Returns config values
        """
        with open (self.path_to_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return ConfigDTO(**config)


    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters
        are not corrupt
        """
        config_dto = self._extract_config_content()

        if not isinstance(config_dto.seed_urls, list):
            raise IncorrectSeedURLError

        for url in config_dto.seed_urls:
            if not isinstance(url, str) or not re.match(r'https?://.*/', url):
                raise IncorrectSeedURLError

        if config_dto.total_articles > NUM_ARTICLES_UPPER_LIMIT:
            raise NumberOfArticlesOutOfRangeError

        if (not isinstance(config_dto.total_articles, int)
                or isinstance(config_dto.total_articles, bool)
                or config_dto.total_articles <= 0):
            raise IncorrectNumberOfArticlesError

        if not isinstance(config_dto.headers, dict):
            raise IncorrectHeadersError

        if not isinstance(config_dto.encoding, str):
            raise IncorrectEncodingError

        if (not isinstance(config_dto.timeout, int)
                or config_dto.timeout < TIMEOUT_LOWER_LIMIT
                or config_dto.timeout > TIMEOUT_UPPER_LIMIT):
            raise IncorrectTimeoutError

        if not isinstance(config_dto.should_verify_certificate, bool) or not isinstance(config_dto.headless_mode, bool):
            raise IncorrectVerifyError

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls
        """
        return self._seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape
        """
        return self._num_articles


    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting
        """
        return self._headers


    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing
        """
        return self._encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response
        """
        return self._timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate
        """
        return self._should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode
        """
        return self._headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Delivers a response from a request
    with given configuration
    """
    headers = config.get_headers()
    timeout = config.get_timeout()
    verify = config.get_verify_certificate()
    response = requests.get(url, headers=headers, timeout=timeout, verify=verify)
    response.encoding = 'utf-8'
    return response

class Crawler:
    """
    Crawler implementation
    """

    url_pattern: Union[Pattern, str]

    def __init__(self, config: Config) -> None:
        """
        Initializes an instance of the Crawler class
        """
        self.seed_urls = config.get_seed_urls()
        self.config = config
        self.urls = []

    def _extract_url(self, article_bs: BeautifulSoup) -> str:
        """
        Finds and retrieves URL from HTML
        """

        url = article_bs.get('href')
        if isinstance(url, str):
            return url
        return ''


    def find_articles(self) -> None:
        """
        Finds articles
        """
        for link in self.seed_urls:
            response = make_request(link, self.config)
            main_bs = BeautifulSoup(response.text, 'lxml')
            for url in main_bs.find_all('a'):
                link = self._extract_url(url)
                if len(self.urls) < self.config.get_num_articles() and link.startswith('news/'):
                    self.urls.append('https://orenday.ru/' + link)

    def get_search_urls(self) -> list:
        """
        Returns seed_urls param
        """
        return self.seed_urls


class HTMLParser:
    """
    ArticleParser implementation
    """

    def __init__(self, full_url: str, article_id: int, config: Config) -> None:
        """
        Initializes an instance of the HTMLParser class
        """
        self.full_url = full_url
        self.article_id = article_id
        self.config = config
        self.article = Article(self.full_url, self.article_id)

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Finds text of article
        """
        article_text = article_soup.find('div', {'itemprop': 'articleBody'})
        text_bs = article_text.find_all('p')
        for t in text_bs:
            self.article.text += t.text


    def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> None:
        """
        Finds meta information of article
        """
        pass

    def unify_date_format(self, date_str: str) -> datetime.datetime:
        """
        Unifies date format
        """
        pass

    def parse(self) -> Union[Article, bool, list]:
        """
        Parses each article
        """
        page = make_request(self.full_url, self.config)
        articles = BeautifulSoup(page.content, "lxml")
        self._fill_article_with_text(articles)
        self._fill_article_with_meta_information(articles)
        return self.article


def prepare_environment(base_path: Union[Path, str]) -> None:
    """
    Creates ASSETS_PATH folder if no created and removes existing folder
    """
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir(parents=True)


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    config = Config(path_to_config=CRAWLER_CONFIG_PATH)
    prepare_environment(ASSETS_PATH)
    crawler = Crawler(config=config)
    crawler.find_articles()
    for idx, url in enumerate(crawler.urls):
        parser = HTMLParser(full_url=url, article_id=idx + 1, config=config)
        text = parser.parse()
        if isinstance(text, Article):
            to_raw(text)


if __name__ == "__main__":
    main()
