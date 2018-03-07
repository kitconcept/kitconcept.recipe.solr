Introduction
============

Buildout recipe to build Solr.

Supported options
=================

The recipe supports the following options:

solr_version (default: latest version)
    Major Solr version

src
    Source of the Solr download.

port (default: 8983)
    Solr port

config
    Custom Solr config XML file


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = solr
    ...
    ... [solr]
    ... recipe = kitconcept.recipe.solr
    ... solr-version = %(src)s
    ... src = %(src)s
    ... port = %(port)s
    ... config = %(config)s
    ... """ % {
    ...     'solr-version': '7',
    ...     'src' : 'http://mirror.netcologne.de/apache.org/lucene/solr/7.2.1/solr-7.2.1.tgz',
    ...     'port' : '8983',
    ...     'config': 'solr.xml',
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
