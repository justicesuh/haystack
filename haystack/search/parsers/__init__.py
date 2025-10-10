from typing import Any

from haystack.search.parsers.base import BaseParser, IPParser
from haystack.search.parsers.linkedin import LinkedInParser


def get_parser(name: str, *args: Any, **kwargs: Any) -> BaseParser:
    """Get `BaseParser` subclass by name."""
    parsers = {
        'ip': IPParser,
        'linkedin': LinkedInParser,
    }
    parser_cls = parsers.get(name)
    if parser_cls is None:
        msg = f'Unknown parser: {name}'
        raise ValueError(msg)
    return parser_cls(*args, **kwargs)
