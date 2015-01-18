from django import template

import csv
import logging
import urllib2

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = 'https://docs.google.com/spreadsheets/d/{key}/export\?format\=csv\&id\={key}'


def get_sheet(key):
    try:
        return urllib2.urlopen(gdocs_format.format(key=key))
    except urllib2.HTTPError as error:
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
