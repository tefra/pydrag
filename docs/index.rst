
pydrag: Fluent Last.fm API Wrapper
==================================


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

----


Why?
----

Just because, I wanted to experiment with python3.6 new features and because I needed a way to access my last.fm data through a library I could understand.

Quick Start
-----------

Apply for an api key from `Last.fm <https://www.last.fm/api/account/create>`_. And write down your API **Key** and **Secret**

Installation::

    pip install pydrag



Simple example
--------------

For most of the read operations you only need to provide your **API KEY**.

All pydrag models always return either a single instance or a list of :class:`~pydrag.lastfm.models.artist.Artist`, :class:`~pydrag.lastfm.models.user.User`, :class:`~pydrag.lastfm.models.track.Track`, :class:`~pydrag.lastfm.models.tag.Tag`, :class:`~pydrag.lastfm.models.album.Album`

Combine that with pydrag's fluent syntax you can do some pretty cool stuff!

.. code-block :: python

    >>> from pydrag import lastfm
    >>> lastfm.configure("<api_key>")
    lets say it worked
    >>> me = lastfm.User.find("Zaratoustre")
    >>> for friend in me.get_friends(recent_tracks=True):
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


Advanced example
----------------

For write operations you need to be authenticated. Last.fm has multiple ways to authenticate users the most simple is to provide your full credentials, but we will dive into authentication later.

Find a track by artist and name, retrieve the album, add some user tags and love the ``Back in Black``

.. code-block :: python

    >>> from pydrag import lastfm

    >>> lastfm.configure("<api_key>", "<api_secret>", "<username>", "<password>")
    lets say it worked
    >>> track = lastfm.Track.find(artist="AC / DC", track="Hells Bell")
    >>> album = track.album
    >>> album.to_dict()
    {'attr': {'position': 1}, 'name': 'Back in Black', 'mbid': '38914b29-7788-4cff-80b7-1ced523f8675', 'url': 'https://www.last.fm/music/AC%2FDC/Back+in+Black', 'image': [{'size'
    : 'small', 'text': 'https://lastfm-img2.akamaized.net/i/u/34s/3d359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'medium', 'text': 'https://lastfm-img2.akamaized.net/i/u/64s/3d
    359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'large', 'text': 'https://lastfm-img2.akamaized.net/i/u/174s/3d359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'extralarge', 'te
    xt': 'https://lastfm-img2.akamaized.net/i/u/300x300/3d359b955132742bc2fc3eacdff90b8c.png'}], 'artist': {'name': 'AC/DC'}}
    >>> full_album_info = track.album.get_info()
    >>>
    >>> full_album_info.add_tags(["awesome", "love"])
    <pydrag.core.BaseModel object at 0x7f38945ac320>
    >>>
    >>> back_in_black = next(track for track in full_album_info.tracks if track.name == "Back in Black")
    >>> write_op = back_in_black.get_info().love()
    >>> write_op.params
    {'method': 'track.love', 'artist': 'AC/DC', 'track': 'Back in Black'}
    >>>


Development
-----------

It's recommended to use `pyenv <https://github.com/pyenv/pyenv>`_ and `pipenv <https://github.com/pypa/pipenv>`_ to manage your local environment.

.. code-block:: console

   $ git clone git@github.com:tefra/pydrag.git
   $ pipenv install . --dev
   $ pipenv run pre-commit install
   $ pipenv run pytest


We use the excellent `vcrpy <https://vcrpy.readthedocs.io/>`_ library to record and replay last.fm responses.

Deleting a recorded response will force the unit-test to perform an actual webservice in order to regenerate the fixture data. All sensitive information like keys and credentials will be automatically censored.

Cassette example ``test/fixtures/track/search.json``.

I also recommend during development to maintain a dotenv file (.env) with your your last.fm configuration, pipenv will pick up the environmental variables and pydrag will create a default configuration for you!

.. code-block:: ini

   LASTFM_API_KEY=e491111111111111111111111111bf35b
   LASTFM_API_SECRET=221b2222222222222222222222292dce
   LASTFM_USERNAME=You
   LASTFM_PASSWORD=YouPass


Table of Contents
-----------------

.. toctree::
    :maxdepth: 3

    usage
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
