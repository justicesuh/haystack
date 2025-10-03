from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver


class Firefox:
    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)

    def get(self, url: str) -> None:
        self.driver.get(url)
        for request in self.driver.requests:
            if request.response:
                print(request.url, request.response.status_code)

    def quit(self) -> None:
        self.drver.quit()
