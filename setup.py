#!/usr/bin/env python

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools

use_setuptools()
from setuptools import setup

execfile(join(dirname(__file__), 'src', 'GuyUtils', 'version.py'))

DESCRIPTION = """
GuyUtils is a handy utility library for Robot Framework
"""[1:-1]

setup(name='robotframework-guyutils',
      version=VERSION,
      description='Utils for Robot Framework',
      long_description=DESCRIPTION,
      author='Guy Kisel',
      author_email='<guy.kisek@gmail.com>',
      url='https://github.com/guykisel/robotframework-guyutils',
      license='MIT',
      keywords='robotframework testing testautomation',
      platforms='any',
      install_requires=[
          'robotframework',
      ],
      py_modules=['ez_setup'],
      package_dir={'': 'src'},
      packages=['GuyUtils'],
      include_package_data=True,
)
