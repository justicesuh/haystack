import logging

from django import template
from django.template.context import Context

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context: Context, name: str) -> str:
    """Return "active" if request path starts with `name`."""
    try:
        if context['request'].path.startswith(name):
            return 'active'
    except Exception:
        logger.exception('Malformed context', stack_info=True)
    return ''
