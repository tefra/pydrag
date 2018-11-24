# pydrag
[![Build Status](https://travis-ci.org/tefra/pydrag.svg?branch=master)](https://travis-ci.org/tefra/pydrag)
[![codecov](https://codecov.io/gh/tefra/pydrag/branch/master/graph/badge.svg)](https://codecov.io/gh/tefra/pydrag)
![GitHub top language](https://img.shields.io/github/languages/top/tefra/pydrag.svg)

pydrag aims to offer a modern interface with fluid syntax for the [last.fm](https://www.last.fm/api) api.


```python
>>> from pydrag.lastfm.models.user import User

>>> me = User.find("Zaratoustre")
>>> recent = me.get_recent_tracks()
# I loved what I heard recently
# lets compile a nice similar playlist :)
>>> more = set([(y.artist.name, y.name)  for x in recent for y in x.get_similar()])

{('10 Years', 'Shoot It Out'),
 ('10 Years', 'Wasteland'),
 ('A Perfect Circle', 'The Outsider'),
 ('Adema', 'Planets'),
 ('Amy Winehouse', 'Back to Black'),
 ('Amy Winehouse', "You Know I'm No Good"),
 ("Anita O'Day", "They Can't Take That Away from Me"),
 ('Aretha Franklin', 'I Say a Little Prayer'),
 ('Aretha Franklin', 'Respect'),
 ('Avenged Sevenfold', 'Natural Born Killer'),
 ('Betty Carter', 'Open The Door'),
 ('Billie Holiday', 'Strange Fruit'),
 ('Billie Holiday', 'Summertime'),
 ('Bob Dylan', 'Like a Rolling Stone'),
 ('Breaking Benjamin', 'So Cold'),
 ('Breaking Benjamin', 'The Diary of Jane'),
 ('Buffalo Springfield', "For What It's Worth"),
 ('Canned Heat', 'On the Road Again'),
...
...

```


## Developing

It's recommended to use [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv)


```python
pipenv install . --dev
pipenv run pre-commit install
pipenv run pytest
```
