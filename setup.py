#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import sheets

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = sheets.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-sheets',
    version=version,
    description="Use Google Sheets as context variables in Django templates",
    long_description=readme + '\n\n' + history,
    author='George Whewell',
    author_email='georgerw@gmail.com',
    url='https://github.com/georgewhewell/django-sheets',
    packages=[
        'sheets',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.5',
        'requests>=2.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-sheets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
