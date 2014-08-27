"""
mezzanine_pagedown is required.
Adds filter 'mkdown' so that any markdown content can be rendered as markdown.
"""

from django import template
from django.utils.safestring import mark_safe
import mezzanine_pagedown.filters as filters

register = template.Library()


@register.filter()
def mkdown(content):
    if content is None:
        return None
    return mark_safe(filters.extra(content))
