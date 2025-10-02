from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from haystack.jobs.models import Location


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('name')
        parser.add_argument('--geo-id', type=int, required=False)

    def handle(self, **options: Any) -> None:
        name, geo_id = options['name'], options['geo_id']
        Location.objects.get_or_create(
            name=name,
            defaults={'geo_id': geo_id},
        )
