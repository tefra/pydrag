Authentication
==============

Apart from your last.fm api key and secret you also need to be authenticated if you wish to perform write operations like scrobbling, adding/removing tags.


Mobile Applications
-------------------

This is what Last.fm calls simple authentication with credentials, it's indented to be used with non-browser application.

Last.fm states that ``Session keys have an infinite lifetime by default``, so generate one and keep using it.


.. code-block :: python

    >>> from pydrag import configure, Album, Config, AuthSession
    >>>
    >>> configurate(api_key='aaaaaaaaaa', api_secret='bbbbbbbbbbb', username='foo', password='bar')
    >>>
    >>>
    >>> session = AuthSession.authenticate()
    >>> session.key
    '2Y5jNDz1111111111111Zq3ZTNjl'
    >>>
    >>>
    >>> configure(api_key='aaaaaaaaaa', api_secret='bbbbbbbbbbb', session='2Y5jNDz1111111111111Zq3ZTNjl')
    >>> album = Album.find_by_mbid("6defd963-fe91-4550-b18e-82c685603c2b")
    >>> album.add_tags(['great', 'rock'])
    >>> Config.instance().session  # store this somewhere and next time
    >>> configurate(api_key='aaaaaaaaaa', api_secret='bbbbbbbbbbb', session='ssssss')


Desktop Application
-------------------

This method is indented for desktop applications, whatever that means.

Step 1: Generate an unauthorized token

.. literalinclude:: /examples/web/app.py
    :linenos:
    :lines: 30-36


Step 2: Send the user to the last.fm site to authorize the token

.. literalinclude:: /examples/web/app.py
    :linenos:
    :lines: 39-44


Step 3:  Retrieve a session with the authorized token

.. literalinclude:: /examples/web/app.py
    :linenos:
    :lines: 47-52



Web Application
---------------

This method is very similar to the above but a lot simpler and makes more sense to me!


Step 1: Send the user to the last.fm site to authorize your application and provide a callback url which will include the authorized token for you!

.. literalinclude:: /examples/web/app.py
    :linenos:
    :lines: 55-64

Step 3:  Retrieve a session with the authorized token

.. literalinclude:: /examples/web/app.py
    :linenos:
    :lines: 47-52


.. note::
    You can find the full demo application built with flask `Here <https://github.com/tefra/pydrag/tree/master/docs/examples/web>`_

    .. code-block:: console

       $ pip install -r docs/examples/web/requirements.txt
       $ FLASK_APP=docs/examples/web/app.py FLASK_DEBUG=1 python -m flask run
