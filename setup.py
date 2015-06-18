#!/usr/bin/env python

from setuptools import setup

setup(name='cryptosync',
      version='0.1',
      description='Personal experiments to sync encrypted data.\
                   Don\'t use it for real world stuff yet.',
      author='Victor Shyba',
      author_email='victor1984@riseup.net',
      url='https://github.com/shyba/cryptosync',
      packages=[
          'cryptosync'
      ],
      test_suite='cryptosync.tests',
      install_requires=[
          'Twisted==15.2.0',
          'leap.auth'
      ],
      tests_require=[
          'mock',
      ],
      )
