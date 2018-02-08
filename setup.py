#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'flask'
]

test_requirements = [
    'pylint',
    'mock',
    'webtest'
]

setup(
    name='flask-deprecate',
    version='0.1.2',
    description="Easy decorators for deprecating flask views and blueprints",
    long_description=readme + '\n\n' + history,
    author="Tim Martin",
    author_email='oss@timmartin.me',
    url='https://github.com/timmartin19/flask-deprecate',
    packages=[
        'flask_deprecate',
    ],
    package_dir={'flask_deprecate':
                 'flask_deprecate'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='flask_deprecate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='flask_deprecate_tests',
    tests_require=test_requirements
)
