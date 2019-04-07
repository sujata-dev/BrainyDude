#!/usr/bin/python3

from setuptools import setup

setup(
    name='BrainyDude',
    packages=['BrainyDude'],
    include_package_data=True,
    install_requires=[
        'flask', 'spacy',
    ],
)
