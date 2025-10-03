from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def get_ip(self, firefox: Firefox) -> str:
        response = firefox.get('https://icanhazip.com/')
        if response is not None:
            soup = firefox.soupify()
            tag = soup.find('pre')
            if tag is not None:
                return tag.text.strip()
        return ''

    def handle(self, **options: Any) -> None:  # noqa: ARG002
        firefox = Firefox(settings.SEARCH_PROXY)
        self.stdout.write(self.get_ip(firefox))
        firefox.create_driver()
        self.stdout.write(self.get_ip(firefox))
