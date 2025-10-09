import logging
from collections.abc import Callable
from typing import cast

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.request import Response

logging.getLogger('seleniumwire').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Firefox:
    """A wrapper around the Selenium Firefox webdriver."""

    def __init__(
        self, request_interceptor: Callable | None = None, response_processor: Callable | None = None
    ) -> None:
        self.request_interceptor = request_interceptor
        self.response_processor = response_processor

        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')

        self.service = Service(executable_path='/usr/local/bin/geckodriver')

        self.create_driver()

    def create_driver(self) -> None:
        """Create Firefox webdriver."""
        self.quit()
        self.driver = webdriver.Firefox(options=self.options, service=self.service)
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

    def soupify(self) -> BeautifulSoup:
        """Parse current page source into BeautifulSoup object."""
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        """End webdriver session."""
        if hasattr(self, 'driver'):
            self.driver.quit()
