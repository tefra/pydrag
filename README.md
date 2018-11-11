# pydrag
[![Build Status](https://travis-ci.org/tefra/pydrag.svg?branch=master)](https://travis-ci.org/tefra/pydrag)
[![codecov](https://codecov.io/gh/tefra/pydrag/branch/master/graph/badge.svg)](https://codecov.io/gh/tefra/pydrag)
![GitHub top language](https://img.shields.io/github/languages/top/tefra/pydrag.svg)

pydrag aims to offer a modern interface for the [last.fm](https://www.last.fm/api) api.


```python
>>> from pydrag.lastfm.services.user import UserService

>>> me = UserService("Zaratoustre")
>>> query = me.get_top_artists(period="7day", limit=5)
>>> while True:
   ...:     print("========= Page:{}/{}, TotalItems: {}.".format(query.page, query.total_pages, query.total))
   ...:     for artist in query.artist:
   ...:         print(artist.name)
   ...:     if not query.has_next():
   ...:         break
   ...:     query = query.get_next()
   ...:

========= Page:1/11, TotalItems: 51.
Red Hot Chili Peppers
Rise Against
All That Remains
Five Finger Death Punch
My Chemical Romance

```


## Developing

It's recommended to use [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv)


```python
pipenv install . --dev
pipenv run pre-commit install
pipenv run pytest
```
