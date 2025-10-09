from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver


class Firefox:
    """A wrapper around the Selenium Firefox webdriver."""

    def __init__(self) -> None:
        options = webdriver.Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)

    def get(self, url: str) -> BeautifulSoup:
        """Naviage to `url` and return page source."""
        self.driver.get(url)
        return self.soupify()

    def soupify(self) -> BeautifulSoup:
        """Parse current page source into BeautifulSoup object."""
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self) -> None:
        """End webdriver session."""
        self.driver.quit()
