#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-sheets
------------

Tests for `django-sheets` models module.
"""

import os
import responses
from io import open

from django import template
from django.test import SimpleTestCase

sample_template = \
    """{% spaceless %}
    {% load sheets %}
    {% csv key as uk500 %}
    <table>
    {% for row in uk500 %}
        <tr>
        {% for cell in row %}
            <td>{{ cell }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </table>
    {% endspaceless %}"""
sample_key = '1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM'
sample_response = os.path.join(
    os.path.dirname(__file__), 'sample_response.csv')
sample_output = os.path.join(
    os.path.dirname(__file__), 'sample_output.html')

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv&id={key}'


class TestSheets(SimpleTestCase):

    def test_no_key(self):
        """
        Empty keys should throw exception
        """
        t = template.Template(sample_template)
        self.assertRaises(RuntimeError, lambda: t.render(template.Context()))
        self.assertEqual(0, len(responses.calls))

    @responses.activate
    def test_404(self):
        """
        Failing to fetch sheet should return empty list
        """
        responses.add(
            responses.GET, gdocs_format.format(key='test'),
            body='404 Not Found', content_type='html/text', status=404,
            match_querystring=True)
        t = template.Template(sample_template)
        self.assertEqual(
            t.render(template.Context({'key': 'test'})),
            '<table></table>')
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_sample_mocked(self):
        responses.add(
            responses.GET, gdocs_format.format(key=sample_key),
            body=open(sample_response, 'rt', encoding='utf-8').read(),
            match_querystring=True, status=200)
        t = template.Template(sample_template)
        output = t.render(template.Context({'key': sample_key}))
        self.assertEqual(1, len(responses.calls))
        self.assertEqual(
            responses.calls[0].request.url,
            gdocs_format.format(key=sample_key))
        self.assertEqual(output, open(sample_output).read())
