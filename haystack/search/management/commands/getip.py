from typing import Any

from django.core.management.base import BaseCommand

from haystack.search.webdriver import Firefox


class Command(BaseCommand):
    def handle(self, **options: Any) -> None:
        """Get ip."""
        firefox = Firefox()
        if firefox.get('https://icanhazip.com/') is not None:
            soup = firefox.soupify()
            if (tag := soup.find('pre')) is not None:
                self.stdout.write(tag.text.strip())
