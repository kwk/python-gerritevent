#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gerritevent",
    version = "1.0",
    author = "Konrad Kleine",
    author_email = "kleine@gonicus.de",
    description = "Library to help implementing gerrit-to-X connectors.",
    long_description = read('README.md'),
    license = 'LGPL',
    keywords = "gerrit api event",
    url = "https://github.com/kwk/python-gerritevent",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Monitoring',
    ],

    packages = find_packages('src', exclude=['examples', 'tests']),
    package_dir={'': 'src'},

    include_package_data = False,
    zip_safe = True,
    install_requires = ["paramiko"]

    #entry_points = """
    #    [console_scripts]
    #    redmine = gerrit.redmine:main
    #""",
)
