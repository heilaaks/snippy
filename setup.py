from setuptools import setup, find_packages

tests_require = ['pytest', 'pytest-cov', 'codecov'],

setup(
    name='snippy',
    version='0.0.1',
    description='A small command line tool to manage command and troubleshooting examples.',
    url='https://github.com/heilaaks/snippy',
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
    entry_points={
        'console_scripts': [
            'snip = snip:main'
        ],
    },
    install_requires=[],
    extras_require={
        'dev': ['pylint', 'pytest', 'pytest-cov', 'sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme'],
        'test': tests_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
