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

sample_key = '1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM'
sample_template = (
    "{% load sheets %}{% csv key as csvrows %}"
    "{% for row in csvrows %}{% for cell in row %}"
    "{{ cell }}{% endfor %}{% endfor %}")

sample_response = os.path.join(
    os.path.dirname(__file__), 'sample_response.csv')
sample_output = os.path.join(
    os.path.dirname(__file__), 'sample_output.txt')

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
        self.assertEqual(t.render(template.Context({'key': 'test'})), '')
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_sample(self):
        responses.add(
            responses.GET, gdocs_format.format(key=sample_key),
            body=open(sample_response, 'rt', encoding='utf-8').read(),
            match_querystring=True, status=200)
        t = template.Template(sample_template)
        output = t.render(template.Context({'key': sample_key}))
        self.assertEqual(
            responses.calls[0].request.url,
            gdocs_format.format(key=sample_key))
        self.assertEqual(1, len(responses.calls))
        self.assertEqual(output, open(sample_output).read())
