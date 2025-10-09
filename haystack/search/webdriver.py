import logging
from typing import cast

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.request import Response

logging.getLogger('seleniumwire').setLevel(logging.WARNING)


class Firefox:
    """A wrapper around the Selenium Firefox webdriver."""

    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)

    def get_last_response(self) -> Response | None:
        """Return `Response` of last driver request."""
        if not self.driver.requests:
            return None
        return cast('Response', self.driver.requests[-1].response)

    def get(self, url: str) -> Response | None:
        """Navigate to `url` and return page source."""
        self.driver.get(url)
        return self.get_last_response()

    def soupify(self) -> BeautifulSoup:
        """Parse current page source into BeautifulSoup object."""
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        """End webdriver session."""
        self.driver.quit()
