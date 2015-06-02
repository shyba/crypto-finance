#!/usr/bin/env python

from setuptools import setup

setup(name='crypto-finance',
      version='0.1',
      description='Soledad encrypted synchronized\
                  local webapp for personal finance',
      author='Victor Shyba',
      author_email='victor1984@riseup.net',
      url='https://github.com/shyba/crypto-finance',
      packages=[
          'crypto_finance'
      ],
      test_suite='crypto_finance.tests',
      install_requires=[
          'Twisted==15.2.0',
          'leap.auth'
      ],
      tests_require=[
          'mock',
      ],
      )
