#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "gerritevent",
    version = "1.0",
    author = "Konrad Kleine",
    author_email = "kleine@gonicus.de",
    description = "Library to help implementing gerrit-to-X connectors.",
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
    #install_requires = ["simplejson"],

    #entry_points = """
    #    [console_scripts]
    #    redmine = gerrit.redmine:main
    #""",
)
