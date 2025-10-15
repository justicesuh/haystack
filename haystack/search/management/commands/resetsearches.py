from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from haystack.search.models import SearchSource, Source


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional source argument."""
        parser.add_argument('--source')

    def handle(self, **options: Any) -> None:
        """Set all SourceSearch.last_executed_at to None."""
        source_name = options['source']
        if source_name is not None:
            try:
                source = Source.objects.get(parser=source_name)
            except Source.DoesNotExist as e:
                msg = f'Source {source_name} does not exist.'
                raise CommandError(msg) from e
            num_updated = SearchSource.objects.filter(source=source).update(last_executed_at=None)
        else:
            num_updated = SearchSource.objects.update(last_executed_at=None)
        self.stdout.write(f'Updated {num_updated} objects.')
