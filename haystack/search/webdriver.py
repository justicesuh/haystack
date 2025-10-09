from selenium import webdriver
from selenium.webdriver.firefox.service import Service


class Firefox:
    """A wrapper around the Selenium Firefox webdriver."""

    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)

    def get(self, url: str) -> str:
        """Naviage to `url` and return page source."""
        self.driver.get(url)
        return self.driver.page_source

    def quit(self) -> None:
        """End webdriver session."""
        self.driver.quit()
