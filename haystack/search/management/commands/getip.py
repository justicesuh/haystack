from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def get_ip(self, firefox: Firefox) -> str:
        """Return IP address."""
        if firefox.get_with_retry('https://icanhazip.com/') is not None:
            soup = firefox.soupify()
            if (tag := soup.find('pre')) is not None:
                return tag.text.strip()
        return ''

    def handle(self, **options: Any) -> None:
        """Demonstrate webdriver by getting IP address."""
        firefox = Firefox(settings.SEARCH_PROXY)
        self.stdout.write(self.get_ip(firefox))
        firefox.create_driver()
        self.stdout.write(self.get_ip(firefox))
