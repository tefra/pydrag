Tag Model
=========


Retrieve tag
-------------

.. code-block :: python

    >>> from pydrag.lastfm import Tag
    >>>
    >>> tag = Tag.find(name="rap", lang="en")
    >>> tag.name
    'rap'
    >>> tag
    Tag(name='rap', reach=100855, url=None, taggings=None, count=None, total=542012, wiki=Wiki(content='Rap is a vocal style, usually coming together with hip-hop, the musical genre off-shoot of the hip hop culture. Rapping itself, also known as emceeing, MCing, spitting, or just rhyming, is the rhythmic spoken delivery of rhymes and wordplay. Rapping is one of the four pillars of the hip hop culture, along with DJing, graffiti, and breaking.\n\nRap is also considered a separate genre from hip hop in some cases where the artists do not make music compatible with the hip hop culture. Some of these cases include Lil Wayne, Juelz Santana, Lil Jon, 50 Cent, T.I., The Game, and Nelly. Rap music has a general focus on pop, hyphy, and snap beats, while hip hop has a general focus on the other four pillars of hip hop. <a href="http://www.last.fm/tag/rap">Read more on Last.fm</a>. User-contributed text is available under the Creative Commons By-SA License; additional terms may apply.', summary='Rap is a vocal style, usually coming together with hip-hop, the musical genre off-shoot of the hip hop culture. Rapping itself, also known as emceeing, MCing, spitting, or just rhyming, is the rhythmic spoken delivery of rhymes and wordplay. Rapping is one of the four pillars of the hip hop culture, along with DJing, graffiti, and breaking.\n\nRap is also considered a separate genre from hip hop in some cases where the artists do not make music compatible with the hip hop culture. <a href="http://www.last.fm/tag/rap">Read more on Last.fm</a>.', published=None, links=None))
    >>>


Get top tags
-------------

.. code-block :: python

    >>> from pydrag.lastfm import Tag
    >>> tags = Tag.get_top_tags(limit=10, page=1)
    >>> [x.name for x in tags]
    ['rock', 'electronic', 'seen live', 'alternative', 'indie', 'pop', 'female vocalists', 'metal', 'alternative rock', 'classic rock']
    >>>


Get top tags chart
------------------

.. code-block :: python

    >>> tags = Tag.get_top_tags_chart(limit=10, page=1)
    >>> tags[0]
    Tag(name='rock', reach=393484, url='https://www.last.fm/tag/rock', taggings=3949977, count=None, total=None, wiki=Wiki(content=None, summary=None, published=None, links=None))




Get similar tags
----------------


.. code-block :: python

    >>> tag = Tag.find(name="rock", lang="en")
    >>> tags = tag.get_similar()
    >>> [x.name for x in tags]
    []
    >>>



Get tag top albums
------------------

.. code-block :: python

    >>> tag = Tag.find(name="rap", lang="en")
    >>> albums = tag.get_top_albums(limit=5)
    >>> [x.name for x in albums]
    ['The Eminem Show', 'Views', 'Relapse', 'The Blueprint 3', 'Beerbongs & Bentleys']
    >>>


Get tag top artists
-------------------

.. code-block :: python

    >>> tag = Tag.find(name="rap", lang="en")
    >>> artists = tag.get_top_artists(limit=5)
    >>> [x.name for x in artists]
    ['Eminem', "Lil' Wayne", '2Pac', 'Dr. Dre', '50 Cent']
    >>>


Get tag top tracks
------------------

.. code-block :: python

    >>> tag = Tag.find(name="rap", lang="en")
    >>> tracks = tag.get_top_tracks(limit=5)
    >>> [x.name for x in tracks]
    ['Stronger', 'Clint Eastwood', 'Lollipop', 'Best I Ever Had', 'Heartless']
    >>>


Get tag weekly chart list
-------------------------

.. code-block :: python

    >>> charts = tag.get_weekly_chart_list()
    >>> charts[0]
    Chart(text='', from_date='1108296000', to_date='1108900800')
    >>> charts[1]
    Chart(text='', from_date='1108900800', to_date='1109505600')
    >>> charts[10]
    Chart(text='', from_date='1114344000', to_date='1114948800')
    >>>
