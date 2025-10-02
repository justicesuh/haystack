from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from haystack.jobs.models import Job, Location
from haystack.search.models import Search


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('keywords')
        parser.add_argument('--location', required=False)
        parser.add_argument('--easy-apply', action='store_true')
        parser.add_argument(
            '--flexibility', choices=[Job.HYBRID, Job.ONSITE, Job.REMOTE], default=Job.ONSITE, required=False
        )

    def handle(self, **options: Any) -> None:
        location = options['location']

        search_kwargs = {
            'keywords': options['keywords'],
            'easy_apply': options['easy_apply'],
            'flexibility': options['flexibility'],
        }

        if location is not None:
            try:
                location_obj = Location.objects.get(name=location)
                search_kwargs['location'] = location_obj
            except Location.DoesNotExist as e:
                msg = f"Location '{location}' does not exist."
                raise CommandError(msg) from e

        Search.objects.get_or_create(**search_kwargs)
