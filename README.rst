Introduction
============

.. image:: https://travis-ci.org/kitconcept/kitconcept.recipe.solr.svg?branch=master
    :target: https://travis-ci.org/kitconcept/kitconcept.recipe.solr

|

.. image:: https://raw.githubusercontent.com/kitconcept/kitconcept.recipe.solr/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/


Buildout recipe for Solr.

Supported options
=================

The recipe supports the following options:

src (required)
    Source of the Solr download (e.g. "http://archive.apache.org/dist/lucene/solr/7.2.1/solr-7.2.1.tgz").

port (default: 8983)
    Solr port

solr-config
    Path to a Solr configuration directory that contains a "core.properties" file and a "data" and "conf" directory.

solr-core-name (default: plone)
    Name of the Solr core. Default is 'plone'.

Example usage
=============

Minimal Buildout
----------------

We'll start by creating a minimal buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = solr
    ...
    ... [solr]
    ... recipe = kitconcept.recipe.solr
    ... src = %(src)s
    ... """ % {
    ...     'src' : 'http://archive.apache.org/dist/lucene/solr/7.2.1/solr-7.2.1.tgz',
    ... })

The only required attribute is `src` that contains a URL of the Solr tgz file.

Running the buildout gives us::

    >>> buildout_output_lower = system(buildout).lower()
    >>> "installing solr" in buildout_output_lower
    True
    >>> import os
    >>> current_path = os.path.dirname(os.path.realpath(__file__))
    >>> full_path = os.path.join(current_path, 'parts/solr/bin/solr')
    >>> os.path.exists(full_path)
    True

    >>> full_path = os.path.join(current_path, 'parts/solr/server/solr/plone')
    >>> os.path.exists(full_path)
    True


Complete Buildout
-----------------

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = solr
    ...
    ... [solr]
    ... recipe = kitconcept.recipe.solr
    ... src = %(src)s
    ... port = %(port)s
    ... solr-config = %(solr-config)s
    ... solr-core-name = %(solr-core-name)s
    ... """ % {
    ...     'src' : 'http://archive.apache.org/dist/lucene/solr/7.2.1/solr-7.2.1.tgz',
    ...     'port' : '8983',
    ...     'solr-config': 'config',
    ...     'solr-core-name': 'solr-core-plone',
    ... })

Running the buildout gives us::

    >>> buildout_output_lower = system(buildout).lower()
    >>> "installing solr" in buildout_output_lower
    True
    >>> import os
    >>> current_path = os.path.dirname(os.path.realpath(__file__))
    >>> full_path = os.path.join(current_path, 'parts/solr/bin/solr')
    >>> os.path.exists(full_path)
    True

    >>> full_path = os.path.join(current_path, 'parts/solr/server/solr/plone')
    >>> os.path.exists(full_path)
    True