from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_str, force_text
from django.utils.functional import cached_property

import csv
import logging
import requests

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv'

CACHE_TIMEOUT = getattr(settings, 'SHEETS_CACHE_TIMEOUT', 300)
CACHE_KEY = 'django-sheets-{key}-{gid}'


class Sheet(object):

    def __init__(self, key, gid):
        if not key:
            raise RuntimeError('Sheet key not supplied')
        self.key = key
        self.gid = gid

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def headers(self):
        return self.data[0] if self.data else []

    def rows(self):
        return self.data[1:] if len(self) > 1 else []

    def _fetch_sheet(self):
        try:
            gdocs_url = gdocs_format.format(key=self.key)
            if self.gid:
                gdocs_url += '&gid={}'.format(self.gid)
            response = requests.get(gdocs_url)
            response.raise_for_status()
            return force_str(response.content)
        except requests.HTTPError as exp:
            logger.error('Error fetching spreadsheet: %s' % exp)
            return force_str('')

    def fetch_sheet(self):
        cache_enabled = not getattr(settings, 'SHEETS_CACHE_DISABLED', False)
        if cache_enabled:
            cache_key = CACHE_KEY.format(
                key=self.key, gid=self.gid)
            cached_output = cache.get(cache_key)

            if cached_output is not None:
                return cached_output

        sheet = self._fetch_sheet()

        if cache_enabled:
            cache.set(cache_key, sheet, CACHE_TIMEOUT)

        return sheet

    @cached_property
    def data(self):
        sheet = self.fetch_sheet()
        reader = csv.reader(
            sheet.splitlines(),
            delimiter=str(','),
            quotechar=str('"'),
            quoting=csv.QUOTE_MINIMAL,
        )
        return [[force_text(cell) for cell in row] for row in reader]


@register.simple_tag(name='csv')
def csv_tag(key, gid=None):
    return Sheet(key, gid)
