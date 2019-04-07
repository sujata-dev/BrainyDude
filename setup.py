#!/usr/bin/python3

from setuptools import setup

setup(
    name='BrainyDudeHeroku',
    packages=['BrainyDudeHeroku'],
    include_package_data=True,
    install_requires=[
        'flask', 'spacy',
    ],
)
