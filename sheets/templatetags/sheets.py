from django import template

import csv
import logging

from django.utils.six.moves.urllib.request import urlopen
from django.utils.six.moves.urllib.error import HTTPError

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = 'https://docs.google.com/spreadsheets/d/{key}/export\?format\=csv\&id\={key}'


def get_sheet(key):
    try:
        return urlopen(gdocs_format.format(key=key))
    except HTTPError as error:
        logger.error("Error fetching url: %s" % error)
        return []

def read_csv(csv_content):
    reader = csv.reader(csv_content)
    return [row for row in reader]

@register.assignment_tag(name='csv')
def csv_tag(key):
    if not key:
        raise RuntimeError('Sheet key not supplied')

    response_data = get_sheet(key)
    return read_csv(response_data)
