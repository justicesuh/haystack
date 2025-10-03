from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:  # noqa: ARG002
        firefox = Firefox()
        response = firefox.get('https://icanhazip.com/')
        if response is not None:
            soup = firefox.soupify()
            tag = soup.find('pre')
            if tag is not None:
                self.stdout.write(tag.text.strip())
