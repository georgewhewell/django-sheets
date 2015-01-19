from __future__ import unicode_literals

from django import template
from django.utils.encoding import force_str, force_text

import csv
import logging
import requests

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv&id={key}'


def get_sheet(key):
    try:
        print(gdocs_format.format(key=key))
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


@register.assignment_tag(name='csv')
def csv_tag(key):
    if not key:
        raise RuntimeError('Sheet key not supplied')

    response_data = get_sheet(key)

    if response_data is None:
        return None

    reader = read_csv(response_data.content)

    return [[force_text(cell) for cell in row] for row in reader]
