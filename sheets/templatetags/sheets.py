from django import template

import csv
import logging
import requests

logger = logging.getLogger(__name__)
register = template.Library()

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv&id={key}'


def get_sheet(key):
    try:
        response = requests.get(gdocs_format.format(key=key))
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as error:
        logger.error("Error fetching url: %s" % error)


def read_csv(csv_content):
    reader = csv.reader(csv_content.text)
    return [row for row in reader]


@register.assignment_tag(name='csv')
def csv_tag(key):
    if not key:
        raise RuntimeError('Sheet key not supplied')

    response_data = get_sheet(key)

    if response_data is None:
        return None

    return read_csv(response_data)
