from setuptools import setup, find_packages

tests_require = ('pytest', 'pytest-cov', 'codecov', 'mock')
docs_require = ('sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme')
exec(open('snippy/version.py').read())

setup(
    name='snippy',
    version=__version__,
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
    url='https://github.com/heilaaks/snippy',
    description='Command line tool to manage command examples and troubleshooting solutions.',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    keywords='cli code command troubleshooting solution manager',
    packages=find_packages(exclude=['tests', 'tests.testlib']),
    package_dir={'snippy': 'snippy'},
    package_data={'snippy': ['data/default/*', 'data/storage/README.md']},
    entry_points={
        'console_scripts': [
            'snippy = snippy.snip:main'
        ],
    },
    install_requires=[],
    extras_require={
        'dev': tests_require + docs_require,
        'test': tests_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
