import os
import sys

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'readme.md')).read()
    CHANGES = open(os.path.join(here, 'changes.txt')).read()
except:
    README = ''
    CHANGES = ''

requires = [
    'nive_cms',
    'pyramid_chameleon'
]

setupkw = dict(
      name='nive_cms_design_bs3',
      version='0.1.1',
      description='Nive cms design based on bootstrap 3',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
      ],
      author='Arndt Droullier, Nive GmbH',
      author_email='info@nive.co',
      url='http://cms.nive.co',
      keywords='bootstrap 3 nive cms website publisher pyramid',
      license='GPL 3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="nive_cms_design_bs3",
)

setup(**setupkw)
