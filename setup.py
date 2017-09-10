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
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console'
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    keywords='cli code command troubleshooting solution manager',
    packages=find_packages(exclude=['tests']),
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
