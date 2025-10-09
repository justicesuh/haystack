from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:
        """Get ip."""
        firefox = Firefox()
        page_source = firefox.get('https://icanhazip.com/')
        self.stdout.write(page_source)
