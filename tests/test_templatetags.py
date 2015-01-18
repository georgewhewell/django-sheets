#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-sheets
------------

Tests for `django-sheets` models module.
"""

import os
import httpretty
from io import open

from django import template
from django.test import SimpleTestCase

    
sample_key = '1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM'
sample_template = '{% load sheets %}{% csv key as csvrows %}{% for row in csvrows %}{% for cell in row %}{{ cell }}{% endfor %}{% endfor %}'
sample_response = os.path.join(os.path.dirname(__file__), 'sample_response.csv')
sample_output = os.path.join(os.path.dirname(__file__), 'sample_output.txt')

gdocs_format = 'https://docs.google.com/spreadsheets/d/{key}/export\?format\=csv\&id\={key}'


class TestSheets(SimpleTestCase):

    def test_no_key(self):
        """
        Empty keys should throw exception
        """
        t = template.Template(sample_template)
        self.assertRaises(RuntimeError, lambda: t.render(template.Context()))

    @httpretty.activate
    def test_404(self):
        """
        Failing to fetch sheet should return empty list
        """
        httpretty.register_uri(httpretty.GET, gdocs_format.format(key='test'),
           body='404 Not Found',
           content_type='html/text',
           status=404)
        t = template.Template(sample_template)
        self.assertEqual(t.render(template.Context({'key': 'test'})), '')

    @httpretty.activate
    def test_sample(self):
        httpretty.register_uri(httpretty.GET, gdocs_format.format(key=sample_key),
           body=open(sample_response, 'rt', encoding='utf-8').read(),
           content_type='text/csv', status=200)
        t = template.Template(sample_template)
        self.assertEqual(t.render(template.Context({'key': sample_key})), open(sample_output).read())
