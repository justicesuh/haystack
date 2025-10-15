from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from haystack.jobs.models import Job
from haystack.search.models import Source
from haystack.search.parsers import get_parser

if TYPE_CHECKING:
    from haystack.search.parsers.base import BaseParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        """Add optional source argument."""
        parser.add_argument('--source')

    def handle(self, **options: Any) -> None:
        """Populate jobs."""
        source_name = options['source']
        if source_name is not None:
            try:
                source = Source.objects.get(parser=source_name)
            except Source.DoesNotExist as e:
                msg = f'Source {source_name} does not exist.'
                raise CommandError(msg) from e
            jobs = Job.objects.filter(status=Job.NEW, populated=False, search_source__source=source)
        else:
            jobs = Job.objects.filter(status=Job.NEW, populated=False, search_source__isnull=False)

        parser_map: dict[str, BaseParser] = {}
        self.stdout.write(f'Populating {len(jobs)} jobs')
        for job in jobs:
            search_source = job.search_source
            if search_source is None:
                # this should never be reached due to queryset but check anyways
                continue
            parser_name = search_source.source.parser
            if parser_name not in parser_map:
                parser_map[parser_name] = get_parser(parser_name)
            parser_map[parser_name].populate_job(job)  # type: ignore[attr-defined]
