from setuptools import setup, find_packages

tests_require = ['pytest', 'pytest-cov'],

setup(
    name='snip',
    version='0.0.1',
    description='Snippet manager for commands and logs.',
    url='https://github.com/heilaaks/snip',
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
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
    keywords='cli code command troubleshooting manager',
    packages=find_packages(exclude=['tests']),
    install_requires=['argparse'],
    entry_points={
        'console_scripts': [
            'snip = snip:main'
        ],
    },
    extras_require={
        'dev': ['pylint', 'pytest', 'pytest-cov', 'sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme'],
        'tests': ['pytest', 'pytest-cov'],
    },
    test_suite='tests',
    tests_require=tests_require,
)
