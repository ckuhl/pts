import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
        name="PythonTestSuite",
        version="0.0.3",  # TODO: Replace this with version string
        packages=['pts'],
        licence="GNU GPLv3",
        scripts=['bin/pts'],
        long_description=open('README.md').read(),
        url='https://github.com/ckuhl/pts',
        maintainer='ckuhl',
        maintainer_email='pts@ckuhl.com',
)

