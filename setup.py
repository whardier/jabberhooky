#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from jabberhooky import __version__

setup(
    name='jabberhooky',
    version=__version__,
    author='Shane R. Spencer',
    author_email='shane@bogomip.com',
    packages=['jabberhooky'],
    url='https://github.com/whardier/jabberhooky',
    license='MIT',
    description='HTTP based keyboard/mouse input',
    long_description=open('README.md').read(),
    install_requires=[
        'tornado>=2.4',
        'sleekxmpp>=1.1.10',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    entry_points={
        'console_scripts': [
            'jabberhooky = jabberhooky.__main__:run',
        ],
    }

)


