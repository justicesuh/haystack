from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from haystack.jobs.models import Job
from haystack.search.models import SearchSource, Source, Status
from haystack.search.parsers import get_parser

if TYPE_CHECKING:
    from haystack.search.parsers.base import BaseParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional source argument."""
        parser.add_argument('--source')

    def handle(self, **options: Any) -> None:
        """Execute job search."""
        source_name = options['source']
        if source_name is not None:
            try:
                source = Source.objects.get(parser=source_name)
            except Source.DoesNotExist as e:
                msg = f'Source {source_name} does not exist.'
                raise CommandError(msg) from e
            search_sources = SearchSource.objects.filter(source=source)
        else:
            search_sources = SearchSource.objects.all()

        total_count = 0
        parser_map: dict[str, BaseParser] = {}
        for search_source in search_sources:
            parser_name = search_source.source.parser
            if parser_name not in parser_map:
                parser_map[parser_name] = get_parser(parser_name)

            self.stdout.write(f'Executing {search_source}')
            search_source.set_status(Status.RUNNING)
            parser = parser_map[parser_name]
            page_count = parser.get_page_count(search_source)  # type: ignore[attr-defined]
            self.stdout.write(f'Found {page_count} pages')
            for page in range(1, page_count + 1):
                self.stdout.write(f'Parsing page {page}')
                jobs = parser.parse(search_source, page)  # type: ignore[attr-defined]
                count = Job.objects.add_jobs(jobs, search_source)
                self.stdout.write(f'Added {count} jobs')
                total_count += count
            search_source.set_status(Status.SUCCESS)

        self.stdout.write(f'Added {total_count} total jobs')
