#!/usr/bin/env python

from distutils.core import setup

setup(name='django-collada',
    version='1.0.3',
    description='A Django application that adds support for uploading and visualizing a Collada model.',
    author='Hans Eklund',
    author_email='hans.eklund@igw.se',
    url='https://github.com/iGW/django-collada',
    packages=[
        'django_collada',
        'django_collada.migrations'
    ],
    requirements=[
        'pycollada==0.4.1'
    ]
)
