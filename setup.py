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

dev_require = ('logging_tree',)
tests_require = ('pytest==3.3.1', 'pytest-cov', 'tox', 'codecov', 'mock', 'six', 'flake8')
docs_require = ('sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme')
server_require = ('falcon==1.3.0', 'gunicorn')
exec(open('snippy/metadata.py').read())

setup(
    name='snippy',
    version=__version__,
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
    url=__homepage__,
    description='Command, solution and code snippet management.',
    long_description='Manage command examples and solutions directly from command line.' +
                     'Snippy tool is intended to support software development and troubleshooting ' +
                     'workflows by collecting command examples and troubleshooting solutions ' +
                     'into one manager.',
    license='GNU AGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU Affero General Public License v3',
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
    package_data={'snippy': ['data/config/*', 'data/default/*', 'data/template/*', 'data/storage/*']},
    entry_points={
        'console_scripts': [
            'snippy = snippy.snip:main'
        ],
    },
    install_requires=['pyyaml'],
    extras_require={
        'dev': dev_require + tests_require + docs_require + server_require,
        'server': server_require,
        'test': tests_require + server_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
