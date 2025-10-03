from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:
        firefox = Firefox()
        response = firefox.get('https://icanhazip.com/')
        if response is not None:
            soup = firefox.soupify()
            print(soup.find('pre').text.strip())
