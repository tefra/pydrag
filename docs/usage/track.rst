Track Model
===========


Retrieve track
--------------

.. code-block :: python

    >>> from pydrag import Track
    >>>
    >>> track = Track.find(artist="AC / DC", track="Hells Bell")
    >>>
    >>> track.name
    'Hells Bells'
    >>> track.album
    Album(attr=RootAttributes(tag=None, page=None, user=None, country=None, total=None, album=None, artist=None, limit=None, track=None, total_pages=None, to_date=None, from_date=None, offset=None, timestamp=None, rank=None, date=None, ignored=None, position=1, accepted=None), name='Back in Black', mbid='38914b29-7788-4cff-80b7-1ced523f8675', url='https://www.last.fm/music/AC%2FDC/Back+in+Black', image=[Image(size='small', text='https://lastfm-img2.akamaized.net/i/u/34s/3d359b955132742bc2fc3eacdff90b8c.png'), Image(size='medium', text='https://lastfm-img2.akamaized.net/i/u/64s/3d359b955132742bc2fc3eacdff90b8c.png'), Image(size='large', text='https://lastfm-img2.akamaized.net/i/u/174s/3d359b955132742bc2fc3eacdff90b8c.png'), Image(size='extralarge', text='https://lastfm-img2.akamaized.net/i/u/300x300/3d359b955132742bc2fc3eacdff90b8c.png')], text=None, playcount=None, artist=Artist(name='AC/DC', mbid=None, url=None, tag_count=None, listeners=None, playcount=None, image=None, match=None, attr=None, tags=None, bio=None, on_tour=None, similar=None, text=None), listeners=None, tags=None, tracks=None, wiki=None)
    >>> track.album.name
    'Back in Black'
    >>>

You can also use MusicBrainz ids to retrieve tracks

.. code-block :: python

    >>> from pydrag import Track
    >>>
    >>> track = Track.find_by_mbid("dfee97091197486fbe21c6217e4a8402")


Search tracks
--------------
.. code-block :: python

    >>> from pydrag import Track
    >>>
    >>> tracks = Track.search(track="wait and bleed")
    >>> [t.name for t in tracks]
    ['Wait and Bleed', 'Wait and Bleed (Terry Date mix)', 'Wait and Bleed [Terry Date Mix]', 'Wait & Bleed', 'Wait and Bleed (live)']



Top tracks by country
---------------------

.. code-block :: python

    >>> from pydrag import Track
    >>>
    >>> tracks = Track.get_top_tracks_by_country(country="italy", limit=5)
    >>> [t.name for t in tracks]
    ['Creep', 'Smells Like Teen Spirit', 'Karma Police', 'Come as You Are', 'Burn the Witch']



Top tracks chart
----------------

.. code-block :: python

    >>> from pydrag import Track
    >>>
    >>> tracks =  Track.get_top_tracks_chart(limit=3)
    >>> [t.name for t in tracks]
    ['Thank U, Next', 'Bohemian Rhapsody - Remastered 2011', 'SICKO MODE']
    >>>


Love / Unlove tracks
--------------------

We probably need to rethink the response for write operations...

.. code-block :: python

    >>> track = Track.find(artist="AC / DC", track="Hells Bell")
    >>> track.love()
    RawResponse(data=None)
    >>>
    >>> track.unlove()
    RawResponse(data=None)


Tracks Tagging
--------------

.. code-block :: python

    >>> track = Track.find(artist="AC / DC", track="Hells Bell")
    >>> track.add_tags(["super", "hot"])
    >>> track.remove_tag("hot")


Update Now Playing
------------------

The response contains various validation messages which don't make much sense...

.. code-block :: python

    >>> status = Track.update_now_playing(track="Hells Bells", artist="AC/DC", track_number=2)
    >>> status.to_dict()
    {'album': {'text': '', 'corrected': 0}, 'artist': {'text': 'AC/DC', 'corrected': 0}, 'track': {'text': 'Hells Bells', 'corrected': 0}, 'ignored_message': {'text': '', 'code': '0'}, 'album_artist': {'text': '', 'corrected': 0}}
    >>>



Scrobble Tracks
----------------

Last.fm has a limit on how many tracks you can scrobble at once, pydrag allows you to take control of the batch size but internally it will max out to 50 tracks per batch.


.. code-block :: python

    >>> from datetime import datetime, timedelta
    >>> import time
    >>> from pydrag import Track
    >>> from pydrag.models.common import ScrobbleTrack
    >>>
    >>> entries = (
    ...     ("Green Day", "Bang Bang"),
    ...     ("Please Fail", "Now"),
    ...     ("The Head and the Heart", "All We Ever Knew"),
    ...     ("Kaleo", "Way Down We Go"),
    ...     ("Disturbed", "The Sound of Silence"),
    ... )
    >>>
    >>> tracks = []
    >>> date = datetime.now()
    >>> for artist, track in entries:
    ...     date = date - timedelta(minutes=5)
    ...     timestamp = int(time.mktime(date.timetuple()))
    ...     tracks.append(
    ...         ScrobbleTrack(artist=artist, track=track, timestamp=timestamp)
    ...     )
    ...
    >>> result = Track.scrobble_tracks(tracks, batch_size=2)
    >>> result.to_dict()
    {'data': [{'artist': 'Green Day', 'track': 'Bang Bang', 'timestamp': 1544365120}, {'artist': 'Please Fail', 'track': 'Now', 'timestamp': 1544364820}, {'artist': 'The Head and the Heart', 'track': 'All We Ever Knew', 'timestamp': 1544364520}, {'artist': 'Kaleo', 'track': 'Way Down We Go', 'timestamp': 1544364220}, {'artist': 'Disturbed', 'track': 'The Sound of Silence', 'timestamp': 1544363920}]}
    >>>

.. caution:: Nothing really fails in the scrobble api

    .. image:: /_static/nothing_fails.png
