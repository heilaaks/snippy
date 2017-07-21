from setuptools import setup, find_packages

setup(
    name='cuma',
    version='0.0.1',
    description='Command Utility Manager for code and command snippets.',
    url='https://github.com/heilaaks/cuma',
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    extras_require={
        'dev': ['pylint', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'cuma = cuma:main'
        ],
    },
)
