"""
pooldcode
========

This is the poold.in private python package index. It is responsible for
authorizing downloads and proxying content from s3.
"""

from setuptools import setup, find_packages
import sys

py = sys.version_info[:2]

if py > (2, 7) or py < (2, 7):
    raise RuntimeError('Python 2.7 is required')


required = [
    'boto==2.6.0',
    'gunicorn==0.14.6',
    'flask==0.9',
]

meta = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Poold.in'
]

setup(name='pooldcode',
      version='0.1.0',
      description='The poold.in private python package index',
      long_description=__doc__,
      keywords='website',
      author='Poold.in',
      author_email='dev@poold.in',
      url='http://code.poold.in',
      license='PRIVATE',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(),
      install_requires=required,
      entry_points=dict(),
      scripts=[],
      classifiers=meta)
