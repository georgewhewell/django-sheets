from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_str, force_text

import csv
import logging
import requests

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv&id={key}'

CACHE_TIMEOUT = getattr(settings, 'SHEETS_CACHE_TIMEOUT', 300)
CACHE_KEY = 'django-sheets-{key}'


def get_sheet(key):
    try:
        response = requests.get(gdocs_format.format(key=key))
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as error:
        logger.error("Error fetching url: %s" % error)


def read_csv(csv_content):
    return csv.reader(
        force_str(csv_content).splitlines(),
        delimiter=str(','),
        quotechar=str('"'),
        quoting=csv.QUOTE_MINIMAL,
    )


class ExplicitNone:
    pass


@register.assignment_tag(name='csv')
def csv_tag(key):
    if not key:
        raise RuntimeError('Sheet key not supplied')

    cache_enabled = not getattr(settings, 'SHEETS_CACHE_DISABLED', False)

    if cache_enabled:
        cache_key = CACHE_KEY.format(key=key)
        cached_output = cache.get(cache_key)
        if cached_output is not None:
            return cached_output

    response_data = get_sheet(key)

    if response_data:
        reader = read_csv(response_data.content)
        response_data = [[force_text(cell) for cell in row] for row in reader]

    if cache_enabled:
        cache.set(cache_key, response_data, CACHE_TIMEOUT)

    return response_data
