pydrag
======


.. image:: https://travis-ci.org/tefra/pydrag.svg?branch=master
        :target: https://travis-ci.org/tefra/pydrag

.. image:: https://codecov.io/gh/tefra/pydrag/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/tefra/pydrag

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black

.. image:: https://img.shields.io/github/languages/top/tefra/pydrag.svg
        :target: https://pydrag.readthedocs.io/

----


What
==========

pydrag aims to offer a modern interface with fluid syntax for the `Last.fm <https://www.last.fm/api/>`_ api.


.. code-block:: python

    >>> from pydrag.lastfm.models.user import User
    >>> rj = User.find("RJ")
    >>> rj.real_name
    'Richard Jones '
    >>> recent = rj.get_recent_tracks()
    >>> first = recent.pop()
    >>> first.name
    'Fu-Gee-La'
    >>> type(first)
    <class 'pydrag.lastfm.models.track.Track'>
    >>> similar = first.get_similar(limit=1)
    >>> similar[0].name
    'Family Business'
    >>> similar[0].artist.name
    'Fugees'
    >>>



Developing
==========

It's recommended to use `pyenv <https://github.com/pyenv/pyenv>`_ and `pipenv <https://github.com/pypa/pipenv>`_

.. code-block:: console

   $ pipenv install . --dev
   $ pipenv run pre-commit instal
   $ pipenv run pytest
