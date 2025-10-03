import logging
from typing import cast

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.request import Response

logging.getLogger('seleniumwire').setLevel(logging.WARNING)


class Firefox:
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)

    def get_last_response(self) -> Response | None:
        request = self.driver.requests[-1] if self.driver.requests else None
        if request is not None:
            return cast('Response', request.response)
        return None

    def get(self, url: str) -> Response | None:
        self.driver.get(url)
        response = self.get_last_response()
        if response is not None:
            return response
        return None

    def soupify(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        self.drver.quit()
