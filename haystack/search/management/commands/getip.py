from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.parsers.base import IPParser


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:
        """Demonstrate webdriver by getting IP address."""
        parser = IPParser()
        self.stdout.write(parser.parse())
        parser.create_driver()
        self.stdout.write(parser.parse())
