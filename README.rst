pydrag
======


.. image:: https://travis-ci.org/tefra/pydrag.svg?branch=master
        :target: https://travis-ci.org/tefra/pydrag

.. image:: https://readthedocs.org/projects/pydrag/badge
    :target: https://pydrag.readthedocs.io/en/latest

.. image:: https://codecov.io/gh/tefra/pydrag/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/tefra/pydrag

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black

.. image:: https://img.shields.io/github/languages/top/tefra/pydrag.svg
        :target: https://pydrag.readthedocs.io/

.. image:: https://api.codacy.com/project/badge/Grade/502de74e87c64d6480749846b161fd62
   :target: https://www.codacy.com/app/tefra/pydrag?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tefra/pydrag&amp;utm_campaign=Badge_Grade

.. image:: https://img.shields.io/pypi/pyversions/pydrag.svg
        :target: https://pypi.org/pypi/pydrag/

.. image:: https://img.shields.io/pypi/v/pydrag.svg
        :target: https://pypi.org/pypi/pydrag/

----


**pydrag** is a modern api wrapper for the `Last.fm <https://www.last.fm/api/>`_ api with a fluent syntax!


Quick Start
-----------

Apply for a last.fm `api key <https://www.last.fm/api/account/create>`_ and write down your **key** and **secret**.

Install
~~~~~~~

.. code-block:: console

    $ pip install pydrag


Example
~~~~~~~

.. code-block:: python

    >>> from pydrag import User, configure
    >>> configure(api_key='54062d8af7afdc_not_real_3459048a4')
    >>> rj = User.find("RJ")
    >>> rj.real_name
    'Richard Jones '
    >>> recent = rj.get_recent_tracks(limit=1, page=1)
    >>> first = recent.pop()
    >>> first.name
    'Fu-Gee-La'
    >>> similar = first.get_similar(limit=1)
    >>> similar[0].name
    'Family Business'
    >>> similar[0].artist.name
    'Fugees'
    >>>
    >>> for friend in rj.get_friends(recent_tracks=True):
    ...     friend.name, friend.recent_track.name
    ...
    ('meichi', 'Pi')
    ('demkod', '(bottle back)')
    ('STBKilla', 'Nowhere Fast')
    ('keret221', 'Letter Home')
    ('Lilfix', 'Namorar pra Quê?')
    ('Yoji', 'Empire State of Mind (feat. Alicia Keys)')
    ('Kastishka', 'Wipe Your Eyes')
    ('comingsoon_', 'I Want It All')
    ('Bagheera', 'Welcome Home')


Development
===========

Use you favorite tool to create a python >= 3.6 virtual environment

.. code-block:: console

   $ git clone git@github.com:tefra/pydrag.git
   $ pip install .[dev]
   $ pre-commit install
   $ pytest
   $ tox

pydrag uses `vcrpy <https://vcrpy.readthedocs.io/>`_ library to record and replay last.fm responses for its unit tests and `python-dotenv <https://pypi.org/project/python-dotenv/>`_ to auto-configure itself.

All sensitive information like keys and credentials are automatically censored.

So when it's necessary to record a new response it's super useful to have a .env file with your configuration!

.. code-block:: ini

   LASTFM_API_KEY=your_api_key
   LASTFM_API_SECRET=your_api_secret
   LASTFM_USERNAME=You
   LASTFM_PASSWORD=YouPass
