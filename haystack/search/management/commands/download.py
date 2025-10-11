from pathlib import Path  # noqa: TC003
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from haystack.search.parsers import get_parser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        """Add parser and url arguments."""
        parser.add_argument('--parser', default='ip')
        parser.add_argument('url')

    def save_html(self, html: str) -> None:
        """Svae html to download folder."""
        download_dir: Path = settings.BASE_DIR.parent / 'download'
        download_dir.mkdir(exist_ok=True)
        with (download_dir / f'{timezone.now()}.html').open('w') as f:
            f.write(html)

    def handle(self, **options: Any) -> None:
        """Get url with given parser and save to file."""
        parser = get_parser(options['parser'])
        if parser.firefox.get_with_retry(options['url']) is not None:
            self.save_html(parser.firefox.driver.page_source)
        parser.quit()
