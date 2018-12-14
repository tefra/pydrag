.. include:: ../README.rst


Advanced example
----------------

For write operations you need to be authenticated. Last.fm has multiple ways to authenticate users the most simple is to provide your full credentials.

Find a track by artist and name, retrieve the album, add some user tags and love the ``Back in Black``

.. code-block :: python

    >>> import pydrag

    >>> pydrag.configure("<api_key>", "<api_secret>", "<username>", "<password>")
    lets say it worked
    >>> track = pydrag.Track.find(artist="AC / DC", track="Hells Bell")
    >>> album = track.album
    >>> album.to_dict()
    {'attr': {'position': 1}, 'name': 'Back in Black', 'mbid': '38914b29-7788-4cff-80b7-1ced523f8675', 'url': 'https://www.last.fm/music/AC%2FDC/Back+in+Black', 'image': [{'size'
    : 'small', 'text': 'https://lastfm-img2.akamaized.net/i/u/34s/3d359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'medium', 'text': 'https://lastfm-img2.akamaized.net/i/u/64s/3d
    359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'large', 'text': 'https://lastfm-img2.akamaized.net/i/u/174s/3d359b955132742bc2fc3eacdff90b8c.png'}, {'size': 'extralarge', 'te
    xt': 'https://lastfm-img2.akamaized.net/i/u/300x300/3d359b955132742bc2fc3eacdff90b8c.png'}], 'artist': {'name': 'AC/DC'}}
    >>> full_album_info = track.album.get_info()
    >>>
    >>> full_album_info.add_tags(["awesome", "love"])
    >>>
    >>> back_in_black = next(track for track in full_album_info.tracks if track.name == "Back in Black")
    >>> write_op = back_in_black.get_info().love()
    >>> write_op.params
    {'method': 'track.love', 'artist': 'AC/DC', 'track': 'Back in Black'}
    >>>


Table of Contents
-----------------

.. toctree::
    :maxdepth: 2
    :numbered:

    usage
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
