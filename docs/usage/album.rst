Album Model
===========


Retrieve album
--------------

.. code-block :: python

    >>> from pydrag import Album
    >>>
    >>> album = Album.find(artist="Queen", album="A Night at the Opera")
    >>> len(album.tracks)
    12
    >>> [x.name for x in album.tracks]
    ['Death on Two Legs (Dedicated to ...)', 'Lazing on a Sunday Afternoon', "I'm in Love With My Car", "You're My Best Friend", "'39", 'Sweet Lady', 'Good Company', 'Seaside Rendezvous', "The Prophet's Song", 'Love of My Life', 'Bohemian Rhapsody', 'God Save the Queen']
    >>>


You can also use MusicBrainz ids to retrieve tracks

.. code-block :: python

    >>> album = Album.find_by_mbid("6defd963-fe91-4550-b18e-82c685603c2b")
    >>> album.listeners
    609001
    >>> album.wiki.summary
    'A Night at the Opera is a 1975 album by English rock band Queen. It was produced by Roy Thomas Baker and Queen, and reportedly was, at the time of its release, the most expensive album ever made. It was originally released by EMI in the UK where it topped the charts for nine weeks, a record at the time, and Elektra Records in the United States where the album peaked at #4 and has been certified Triple Platinum (three million copies sold).\nThe album takes its name from the Marx Brothers film of the same name <a href="http://www.last.fm/music/Queen/A+Night+at+the+Opera">Read more on Last.fm</a>.'
    >>>



Search albums
-------------
.. code-block :: python

    >>> result = Album.search("fire", limit=5)
    >>> [x.name for x in result]
    ['Room on Fire', 'Holy Fire', 'Friendly Fires', 'I Am... Sasha Fierce', 'The Suburbs']
    >>>



Album Tagging
--------------

.. code-block :: python

    >>> album = Album.find(artist="Queen", album="A Night at the Opera")
    >>> album.add_tags(["super", "hot"])
    >>> album.remove_tag("hot")


Get user album tags
-------------------

.. code-block :: python

    >>>
    >>> tags = album.get_tags(user="Zaratoustre")
    >>> [x.name for x in tags]
    ['foo']
    >>>



Get top album tags
------------------

Fix me!!!!

.. code-block :: python

    >>> album = Album.find(artist="Queen", album="A Night at the Opera")
    al>>> tags = album.get_top_tags()
    >>> [x.name for x in tags]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'Tag' object is not iterable
    >>> tags
    Tag(name=6, reach=None, url=None, taggings=None, count=None, total=None, wiki=None)
    >>>
