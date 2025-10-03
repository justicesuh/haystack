# ruff: noqa: E402

import logging
import warnings

warnings.filterwarnings(
    'ignore',
    r'^pkg_resources is deprecated as an API',
    category=UserWarning,
)

from typing import cast

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.request import Response

logging.getLogger('seleniumwire').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Firefox:
    def __init__(self, proxy: str | None = None, request_interceptor=None, response_processor=None) -> None:
        self.request_interceptor = request_interceptor
        self.response_processor = response_processor

        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')

        self.service = Service(executable_path='/usr/local/bin/geckodriver')

        self.seleniumwire_options: dict[str, dict[str, str]] | None
        if proxy is not None:
            self.seleniumwire_options = {
                'proxy': {
                    'http': proxy,
                    'https': proxy,
                    'no_proxy': 'localhost,127.0.0.1',
                }
            }
        else:
            self.seleniumwire_options = None

        self.create_driver()

    def create_driver(self) -> None:
        self.quit()
        self.driver = webdriver.Firefox(
            options=self.options, service=self.service, seleniumwire_options=self.seleniumwire_options
        )
        if self.request_interceptor is not None:
            self.driver.request_interceptor = self.request_interceptor

    def get_last_response(self) -> Response | None:
        request = self.driver.requests[-1] if self.driver.requests else None
        if request is not None:
            return cast('Response', request.response)
        return None

    def get(self, url: str) -> Response | None:
        logger.info('GET %s', url)
        self.driver.get(url)
        if self.response_processor is not None:
            response = self.response_processor(self.driver.requests)
        else:
            response = self.get_last_response()
        if response is None or response.status_code in [403, 404, 429, 500, 501, 502, 503, 504]:
            return None
        return response

    def soupify(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        if hasattr(self, 'driver'):
            self.driver.quit()
