#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-sheets
------------

Tests for `django-sheets` models module.
"""
import os
import codecs

from vcr_unittest import VCRTestCase

from django import template
from django.utils.encoding import force_str
from django.test import override_settings
from django.core.cache import cache

sample_template = \
    """{% spaceless %}
    <html>
    <head>
    <meta charset="utf-8">
    </head>
    {% load sheets %}
    {% csv key as data %}
    <table>
        <thead>
        <tr>
            {% for header in data.headers %}
            <th>{{ header }}</th>
            {% endfor %}
        </tr>
        </thead>
    <tbody>
        {% for row in data.rows %}
        <tr>
            {% for cell in row %}
                <td>{{ cell }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    </html>
    {% endspaceless %}"""
sample_key = '1uPsdcGUnUsf3d2xGHRGUUb7_k5IQPtBvfQY61u8Z8wE'
sample_gid = '1389904005'
sample_response = os.path.join(
    os.path.dirname(__file__), 'sample_response.csv')
sample_output = os.path.join(
    os.path.dirname(__file__), 'sample_output.html')

gdocs_format = \
    'https://docs.google.com/spreadsheets/d/{key}/export?format=csv'


class TestSheets(VCRTestCase):

    def setUp(self):
        super(TestSheets, self).setUp()
        cache.clear()

    def test_no_key(self):
        """
        Empty keys should throw exception
        """
        t = template.Template(sample_template)
        self.assertRaises(RuntimeError, lambda: t.render(template.Context()))

    def test_404(self):
        """
        Failing to fetch sheet should return empty list
        """
        t = template.Template(sample_template)
        self.assertEqual(
            t.render(template.Context({'key': 'test'})),
            '<html><head><meta charset="utf-8"></head>'
            '<table><thead><tr></tr></thead><tbody></table></html>')

    def test_sample_sheet(self):
        """
        Tests a request against live API
        """
        t = template.Template(sample_template)
        output = t.render(template.Context({'key': sample_key}))
        self.assertEqual(force_str(output), codecs.open(sample_output).read())

    def test_sample_sheet_with_gid(self):
        """
        Tests a request with gid parameter to live API
        should return second sheet
        """
        t = template.Template(
            '{% load sheets %}{% csv key gid=gid as data %}'
            '{% for row in data %}'
            '{% for cell in row %}'
            '{{ cell }}'
            '{% endfor %}{% endfor %}')
        output = t.render(
            template.Context({'key': sample_key, 'gid': sample_gid}))
        self.assertEqual(output, 'This is Sheet 2')

    def test_cache(self):
        """
        When cache enabled, rendering tag twice should issue one request
        """
        t = template.Template(sample_template)
        t.render(template.Context({'key': sample_key}))
        t.render(template.Context({'key': sample_key}))
        self.assertEqual(1, len(self.cassette))

    def test_cache_lazy(self):
        """
        tag should not cause http request if never accessed
        """
        t = template.Template('{% load sheets %}{% csv key as data %}Hello')
        t.render(template.Context({'key': sample_key}))
        self.assertEqual(0, len(self.cassette))

    @override_settings(SHEETS_CACHE_DISABLED=True)
    def test_cache_disabled(self):
        """
        When cache disabled, rendering tag twice should issue two requests
        """
        t = template.Template(sample_template)
        t.render(template.Context({'key': sample_key}))
        t.render(template.Context({'key': sample_key}))
        self.assertEqual(2, len(self.cassette))

    def test_cache_when_empty(self):
        """
        Make sure that empty spreadsheets are not mistaken for cache miss
        """
        t = template.Template(sample_template)
        t.render(template.Context({'key': sample_key}))
        t.render(template.Context({'key': sample_key}))
        self.assertEqual(1, len(self.cassette))
