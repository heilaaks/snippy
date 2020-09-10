# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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


REQUIRES = (
    'colorama ; sys_platform == "win32"',
    'importlib_metadata ; python_version!="3.4"',        # To get tox to install in Python 3.4.
    'importlib_metadata==0.23 ; python_version=="3.4"',  # To get tox to install in Python 3.4.
    'pyyaml      ; python_version!="3.4"',
    'pyyaml<=5.2 ; python_version=="3.4"',
)
EXTRAS_SERVER = (
    'falcon==2.0.0',
    'gunicorn==19.10.0 ; python_version<="3.3"',
    'gunicorn==20.0.4  ; python_version>="3.4"',
    'jsonschema==3.2.0',
    'psycopg2==2.8.5 ; platform_python_implementation=="CPython"',
    'psycopg2cffi==2.8.1 ; platform_python_implementation=="PyPy"',
    'pyrsistent==0.16 ; python_version=="2.7" or python_version=="3.4"',  # To get jsonschema to install in Python 2.7 and 3.4.
)
EXTRAS_DEV = (
    'colorama        ; python_version!="3.4"',  # To get openapi2jsonschema to install in Python 3.4.
    'colorama==0.4.1 ; python_version=="3.4"',  # To get openapi2jsonschema to install in Python 3.4.
    'openapi2jsonschema==0.9.0 ; python_version<="3.6"',
    'openapi2jsonschema==0.9.1 ; python_version>="3.7"',
)
EXTRAS_DOCS = (
    'sphinx==1.8.5 ; python_version<="3.4"',
    'sphinx==3.0.0 ; python_version>="3.5"',
    'sphinxcontrib-openapi==0.6.0',
    'sphinx_rtd_theme==0.4.3',
    'sphinx-autobuild==0.7.1',
)
EXTRAS_RELEASE = (
    'readme-renderer      ; python_version!="3.4"',  # To get twine to install in Python 3.4.
    'readme-renderer<25.0 ; python_version=="3.4"',  # To get twine to install in Python 3.4.
    'setuptools',
    'twine       ; python_version!="3.4"',
    'twine<2.0.0 ; python_version=="3.4"',
    'wheel',
)
EXTRAS_TEST = (
    'bandit==1.6.2',
    'docker==4.2.0 ; python_version=="2.7.*" or python_version>="3.5"',
    'docker==3.7.3 ; python_version=="3.4.*"',
    'flake8==3.7.9',
    'logging_tree==1.8.1',
    'mock==3.0.5 ; python_version<="3.5"',
    'mock==4.0.2 ; python_version>="3.6"',
    'pluggy==0.13.1',
    'pprintpp==0.4.0',
    'pyflakes==2.1.1',
    'pylint==1.9.5 ; python_version=="2.7.*"',
    'pylint==2.3.1 ; python_version=="3.4.*"',
    'pylint==2.4.4 ; python_version>="3.5"',
    'pytest==4.6.9 ; python_version<="3.4"',
    'pytest==5.4.1 ; python_version>="3.5"',
    'pytest-cov==2.8.1',
    'pytest-mock==2.0.0 ; python_version<="3.4"',
    'pytest-mock==3.0.0 ; python_version>="3.5"',
    'pytest-xdist==1.31.0',
    'requests',
    'tox==3.14.6 ; python_version=="2.7.*" or python_version>="3.5"',
    'tox==3.14.0 ; python_version=="3.4.*"',
)

META = {}
HERE = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(HERE, 'snippy', 'meta.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), META)  # pylint: disable=exec-used

with io.open('README.rst', mode='r', encoding='utf-8') as f:
    README = f.read()

setup(
    name=META['__title__'],
    version=META['__version__'],
    description=META['__description__'],
    long_description=README,
    long_description_content_type='text/x-rst',
    author=META['__author__'],
    author_email=META['__email__'],
    url=META['__homepage__'],
    license=META['__license__'],
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
    install_requires=REQUIRES,
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
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
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
        'devel': EXTRAS_DEV + EXTRAS_DOCS + EXTRAS_SERVER + EXTRAS_TEST,
        'docs': EXTRAS_DOCS,
        'release': EXTRAS_RELEASE,
        'server': EXTRAS_SERVER,
        'test': EXTRAS_SERVER + EXTRAS_TEST,
    },
    platforms=["Linux", "MacOS", "Microsoft"],
    tests_require=EXTRAS_TEST,
    test_suite='tests'
)
