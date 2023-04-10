"""
Crawler implementation
"""
import datetime
import json
from pathlib import Path
from typing import Pattern, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from core_utils.article.article import Article
from core_utils.article.io import to_meta, to_raw
from core_utils.config_dto import ConfigDTO
from core_utils.constants import (ASSETS_PATH, CRAWLER_CONFIG_PATH,
                                  NUM_ARTICLES_UPPER_LIMIT,
                                  TIMEOUT_LOWER_LIMIT, TIMEOUT_UPPER_LIMIT)

class IncorrectSeedURLError(Exception):
pass


class NumberOfArticlesOutOfRangeError(Exception):
pass

class IncorrectNumberOfArticlesError(Exception):
pass

class IncorrectHeadersError(Exception):
pass

class IncorrectEncodingError(Exception):
pass

class IncorrectTimeoutError(Exception):
pass

class IncorrectVerifyError(Exception):
pass

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
        configDTO = self._extract_config_content()
        self._seed_urls = configDTO.seed_urls
        self._num_articles = configDTO.total_articles
        self._headers = configDTO.headers
        self._encoding = configDTO.encoding
        self._timeout = configDTO.timeout
        self._should_verify_certificate = configDTO.should_verify_certificate
        self._headless_mode = configDTO.headless_mode

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
        with open(self.path_to_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        seed_urls = config['seed_urls']
        headers = config['headers']
        total_articles_to_find_and_parse = config['total_articles_to_find_and_parse']
        encoding = config['encoding']
        timeout = config['timeout']
        verify_certificate = config['should_verify_certificate']
        headless_mode = config['headless_mode']

        pass

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls
        """
        return configDTO.seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape
        """
        return configDTO.total_articles


    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting
        """
        return configDTO.headers


    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing
        """
        return configDTO.encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response
        """
        return configDTO.timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate
        """
        return configDTO.should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode
        """
        return configDTO.headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Delivers a response from a request
    with given configuration
    """
    headers = config.get_headers()
    return  requests.get(url, headers=headers)


class Crawler:
    """
    Crawler implementation
    """

    url_pattern: Union[Pattern, str]

    def __init__(self, config: Config) -> None:
        """
        Initializes an instance of the Crawler class
        """
        self.config = config
        self.urls = []

    def _extract_url(self, article_bs: BeautifulSoup) -> str:
        """
        Finds and retrieves URL from HTML
        """

        link = article_bs.get('href')
        if (link is not None) and
        pass

    def find_articles(self) -> None:
        """
        Finds articles
        """
        for link_bs in self.config._extract_config_content().get_seed_urls:
            link = link_bs.get('href')
            if link is None:  # no ==
                continue
            elif link[0] == 'n' and link[1] == 'e' and link[2] == 'w' and link.count('#') == 0 and link.count('?') == 0:
                self.urls.append('https://orenday.ru/' + link_bs['href'])
        pass

    def get_search_urls(self) -> list:
        """
        Returns seed_urls param
        """
        return self.config._extract_config_content().get_seed_urls


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
        pass

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Finds text of article
        """
        article_text = main_bs.find('div', {'itemprop': 'articleBody'})
        article_soup = article_text.find_all('p')
        #for t in text_bs:
            #print(t.text)
        pass

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
        pass


def prepare_environment(base_path: Union[Path, str]) -> None:
    """
    Creates ASSETS_PATH folder if no created and removes existing folder
    """
    pass


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    pass


if __name__ == "__main__":
    main()
