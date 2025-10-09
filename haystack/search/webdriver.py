import logging
import time
from collections.abc import Callable
from copy import deepcopy
from typing import cast

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.request import Response

logging.getLogger('seleniumwire').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Firefox:
    """A wrapper around the Selenium Firefox webdriver."""

    def __init__(
        self,
        proxy: str | None = None,
        request_interceptor: Callable | None = None,
        response_processor: Callable | None = None,
    ) -> None:
        self.request_interceptor = request_interceptor
        self.response_processor = response_processor

        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')

        self.service = Service(executable_path='/usr/local/bin/geckodriver')

        self.seleniumwire_options: dict[str, dict[str, str]] | None = None
        if proxy is not None:
            self.seleniumwire_options = {
                'proxy': {
                    'http': proxy,
                    'https': proxy,
                    'no_proxy': 'localhost,127.0.0.1',
                }
            }

        self.driver = None
        self.create_driver()

    def create_driver(self) -> None:
        """Create Firefox webdriver.

        Deepcopy of `self.seleniumwire_options` is required because
        upstream proxy configuration destroys original dictionary.

        See https://github.com/wkeeling/selenium-wire/blob/da1b675fe2cc6dae2e3bb959c1ce95eb1c41830b/seleniumwire/utils.py#L24
        for more details.
        """
        self.quit()
        self.driver = webdriver.Firefox(
            options=self.options, service=self.service, seleniumwire_options=deepcopy(self.seleniumwire_options)
        )
        if self.request_interceptor is not None:
            self.driver.request_interceptor = self.request_interceptor

    def get_last_response(self) -> Response | None:
        """Return `Response` of last driver request."""
        if (request := self.driver.last_request) is not None:
            return cast('Response', request.response)
        return None

    def get(self, url: str) -> Response | None:
        """Navigate to `url` and return page source."""
        logger.info('GET %s', url)
        self.driver.get(url)
        if self.response_processor is not None:
            response = self.response_processor(self.driver.requests)
        else:
            response = self.get_last_response()
        if response is None or response.status_code in [403, 404, 429, 500, 501, 502, 503, 504]:
            return None
        return response

    def get_with_retry(self, url: str, retries: int = 8, backoff_factor: int = 1) -> Response | None:
        """Retrieve url using exponential backoff."""
        for attempt in range(retries):
            try:
                if (response := self.get(url)) is not None:
                    return response
                self.create_driver()
            except WebDriverException:
                logger.warning('Attempt %d failed for %s', attempt + 1, url)
                self.create_driver()
            backoff = backoff_factor * (2**attempt)
            logger.info('Sleeping for %d seconds', backoff)
            time.sleep(backoff)
        logger.warning('Max retries for %s exceeded', url)
        return None

    def soupify(self) -> BeautifulSoup:
        """Parse current page source into BeautifulSoup object."""
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        """End webdriver session."""
        if self.driver is None:
            return
        try:
            if getattr(self.driver, 'session_id', None):
                self.driver.quit()
            else:
                logger.info('Webdriver session already closed')
        except WebDriverException as e:
            logger.warning('Issue quiting webdriver session: %s', e)
        finally:
            self.driver = None
