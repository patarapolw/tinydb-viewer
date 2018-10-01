# tinydb-viewer

[![PyPI version shields.io](https://img.shields.io/pypi/v/tinydb-viewer.svg)](https://pypi.python.org/pypi/tinydb-viewer/)
[![PyPI license](https://img.shields.io/pypi/l/tinydb-viewer.svg)](https://pypi.python.org/pypi/tinydb-viewer/)

View records generated from [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) and alike (e.g. list of dictionaries.)

## Installation

Method 1:

```commandline
$ pip install tinydb-viewer
```

Method 2:

- Clone the project from GitHub
- [Get poetry](https://github.com/sdispater/poetry) and `poetry install tinydb-viewer --path PATH/TO/TINYDB/VIEWER`

## Usage

Run a server initiation script first. This will allow you to edit the data as well.

```python
from tinydb_viewer import TinyDB
TinyDB('db.json').runserver()
```

Then, in IPython or in Jupyter Notebook,

```python
>>> from tinydb_viewer import TinyDB
>>> tdb = TinyDB('db.json')
>>> tdb.search(tdb.query['foo'] == 'bar', sort_func=lambda x: x['baz'])
>>> tdb.view()
'The first page is shown.'
>>> tdb.view(-1)
'The last page is shown.'
>>> tdb.previous()
'The previous page (i-1) is shown.'
>>> tdb.next()
'The next page (i+1) is shown.'
```

## Bonus

I extended TinyDB a little. My TinyDB is `'ensure_ascii' = False` by default, so that the file is a little smaller.

Also, it will use [tinydb-constraint](https://github.com/patarapolw/tinydb-constraint) by default, if it is installed.

## Screenshots

![](/screenshots/jupyter0.png?raw=true)

## Related projects

- [tinydb-constraint](https://github.com/patarapolw/tinydb-constraint) - Apply constraints before inserting and updating TinyDB records.
