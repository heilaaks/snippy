# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""setup: Install Snippy tool."""

import io
import os
from setuptools import setup, find_packages


requires = (
    'pyyaml',
    'importlib_metadata',
    'colorama ; sys_platform == "win32"'
)
extras_server = (
    'falcon==2.0.0',
    'gunicorn==19.9.0',
    'jsonschema==3.0.1',
    'psycopg2==2.8.3 ; platform_python_implementation=="CPython"',
    'psycopg2cffi==2.8.1 ; platform_python_implementation=="PyPy"'
)
extras_dev = (
    'logging_tree==1.8',
    'openapi2jsonschema==0.9.0'
)
extras_docs = (
    'sphinx==1.8.5 ; python_version<="3.4"',
    'sphinx==2.1.2 ; python_version>"3.4"',
    'sphinxcontrib-openapi==0.4.0',
    'sphinx_rtd_theme==0.4.3',
    'sphinx-autobuild==0.7.1'
)
extras_test = (
    'bandit==1.6.0',
    'docker==4.0.2 ; python_version>"3.4"',
    'docker==4.0.2 ; python_version=="2.7.*"',
    'docker==3.7.2 ; python_version=="3.4.*"',
    'flake8==3.7.7',
    'logging_tree==1.8',
    'mock==3.0.5',
    'pluggy==0.12.0',
    'pprintpp==0.4.0',
    'pyflakes==2.1.1',
    'pylint==1.9.4 ; python_version=="2.7.*"',
    'pylint==2.3.1 ; python_version>"2.7"',
    'pytest==4.6.4 ; python_version<="3.4"',
    'pytest==5.0.0 ; python_version>"3.4"',
    'pytest-cov==2.7.1',
    'pytest-mock==1.10.4',
    'pytest-xdist==1.29.0',
    'requests',
    'tox==3.13.1'
)

meta = {}
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'snippy', 'meta.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), meta)

with io.open('README.rst', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=meta['__title__'],
    version=meta['__version__'],
    description=meta['__description__'],
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=meta['__author__'],
    author_email=meta['__email__'],
    url=meta['__homepage__'],
    license=meta['__license__'],
    keywords='notes markdown yaml text command-line cli server backend docker software-engineering',
    packages=find_packages(exclude=['tests', 'tests.lib']),
    package_dir={'snippy': 'snippy'},
    package_data={
        'snippy': [
            'data/completion/*',
            'data/defaults/*',
            'data/server/openapi/schema/*',
            'data/storage/*',
            'data/templates/*'
        ]
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'snippy = snippy.snip:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities'
    ],
    extras_require={
        'devel': extras_dev + extras_docs + extras_server + extras_test,
        'docs': extras_docs,
        'server': extras_server,
        'test': extras_server + extras_test,
    },
    tests_require=extras_test,
    test_suite='tests'
)
