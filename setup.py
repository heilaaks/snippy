#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

from snippy.meta import __author__
from snippy.meta import __email__
from snippy.meta import __homepage__
from snippy.meta import __license__
from snippy.meta import __version__


dev_require = (
    'logging_tree==1.7',
    'openapi2jsonschema==0.7.0'
)
docs_require = (
    'sphinx==1.7.0',
    'sphinxcontrib-openapi==0.3.2',
    'sphinx_rtd_theme==0.2.4',
    'sphinx-autobuild==0.7.1'
)
server_require = (
    'falcon==1.3.0',
    'gunicorn==19.7.1',
    'schema==0.6.7'
)
tests_require = (
    'codecov==2.0.15',
    'flake8==3.5.0',
    'mock==2.0.0',
    'pytest==3.3.2',
    'pytest-cov==2.5.1',
    'six==1.11.0',
    'tox==2.9.1'
)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'snippy',
    version = __version__,
    author = __author__,
    author_email = __email__,
    url = __homepage__,
    description = 'Command, solution and code snippet management.',
    long_description = readme(),
    license=__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    keywords='command solution snippet manager console',
    packages=find_packages(exclude=['tests', 'tests.testlib']),
    package_dir={'snippy': 'snippy'},
    package_data={'snippy': [
        'data/config/*',
        'data/default/*',
        'data/storage/*'
        'data/template/*',
        ]
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'snippy = snippy.snip:main'
        ],
    },
    install_requires=['pyyaml==3.12'],
    extras_require={
        'dev': dev_require + tests_require + docs_require + server_require,
        'docs': docs_require,
        'server': server_require,
        'test': tests_require + server_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
