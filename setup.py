from setuptools import setup, find_packages

tests_require = ('pytest', 'pytest-cov', 'tox', 'codecov', 'mock', 'six', 'flake8')
docs_require = ('sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme')
exec(open('snippy/version.py').read())

setup(
    name='snippy',
    version=__version__,
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
    url='https://github.com/heilaaks/snippy',
    description='Command and solution example management from terminal.',
    long_description='Manage command examples and solutions directly from command line.',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux'
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    keywords='command solution snippet manager terminal',
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
        'dev': tests_require + docs_require,
        'test': tests_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
