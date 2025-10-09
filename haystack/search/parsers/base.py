import logging
from typing import ClassVar, cast

from django.conf import settings
from seleniumwire.request import Request, Response

from haystack.search.webdriver import Firefox

logger = logging.getLogger(__name__)

firefox_blocklist: list[str] = []


class BaseParser:
    """Base class for managing Firefox based web scraping."""

    blocklist: ClassVar[list[str]] = []

    def __init__(self) -> None:
        self.firefox = Firefox(settings.SEARCH_PROXY, self.intercept_request, self.process_response)

    def intercept_request(self, request: Request) -> None:
        """Abort request if host is in blocklist."""
        if request.host in firefox_blocklist + self.blocklist:
            request.abort(error_code=404)
        else:
            logger.info('Intercepting %s', request.host)

    def process_response(self, requests: list[Request]) -> Response | None:
        """Traverse requests in reverse and return first valid response."""
        if requests is None:
            return None
        for request in reversed(requests):
            response = cast('Response', request.response)
            if response is None or response.status_code == 404:
                continue
            return response
        return None

    def create_driver(self) -> None:
        """Create Firefox driver."""
        self.firefox.create_driver()

    def quit(self) -> None:
        """Quit webdriver session."""
        self.firefox.quit()


class IPParser(BaseParser):
    """A class to demonstrate webdriver by getting IP address."""

    def parse(self) -> str:
        """Return IP address."""
        if self.firefox.get_with_retry('https://icanhazip.com/') is not None:
            soup = self.firefox.soupify()
            if (tag := soup.find('pre')) is not None:
                return tag.text.strip()
        return ''
