# tinydb-viewer

View records generated from [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) and alike (e.g. list of dictionaries.)

## Installation

- Clone the project from GitHub
- Navigate to the project folder, then `poetry install`

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

I extended TinyDB a little. My TinyDB is 'ensure_ascii' = False by default, so that the file is a little smaller.

```python
>>> from tinydb_viewer import TinyDB
>>> tdb = TinyDB('db.json')
>>> schema = tdb.schema()
>>> schema
{'_default': {'patho_id': <class 'str'>, 'patient_id': <class 'int'>, 'full_name': <class 'str'>, 'pathologist': <class 'str'>, 'resident': <class 'str'>, 'received': 'datetime str'}}
```

To ensure consistent types:

```python
>>> tdb.insert_multiple(records, sanitize=True)
```

Default is `sanitize=True`.

## Screenshots

![](/screenshots/jupyter0.png?raw=true)
