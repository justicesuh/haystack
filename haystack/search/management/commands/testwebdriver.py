from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:
        firefox = Firefox()
        firefox.get('https://icanhazip.com/')
