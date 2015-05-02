#!/usr/bin/env python

from distutils.core import setup

setup(name='py1090',
      version='1.0a1',
      description='ADS-B messages from BaseStation handled in a pythonic way.',
      author='Jonas Lieb',
      author_email='jonas@jonaslieb.com',
      url='http://www.jonaslieb.com/',
      packages=['py1090'],
      requires=[],
      license=['Apache License, Version 2.0'],
      classifiers=[
      	'Development Status :: 3 - Alpha',
      	'Intended Audience :: Education',
      	'Intended Audience :: Science/Research',
      	'License :: OSI Approved :: Apache Software License',
      	'Programming Language :: Python :: 3',
      	'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
      ]
	)