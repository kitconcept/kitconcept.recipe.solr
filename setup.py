# -*- coding: utf-8 -*-
"""
This module contains the tool of kitconcept.recipe.solr
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '1.0.0a3'
description = "Buildout recipe for Solr."

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '======================\n'
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '==============\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '========\n')

entry_point = 'kitconcept.recipe.solr:Recipe'
entry_points = {
    "zc.buildout": ["default = %s" % entry_point],
}

tests_require = [
  'zope.testing',
  'zc.buildout[test]',
  'mocker'
]

setup(
    name='kitconcept.recipe.solr',
    version=version,
    description=description,
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    keywords='plone buildout solr',
    author='kitconcept GmbH',
    author_email='info@kitconcept.com',
    url='https://github.com/kitconcept/kitconcept.recipe.solr',
    license='gpl',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['kitconcept', 'kitconcept.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        'collective.recipe.template',
        'hexagonit.recipe.download',
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='kitconcept.recipe.solr.tests.test_docs.test_suite',
    entry_points=entry_points,
)
