# tinydb-viewer

View records generated from [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) and alike (e.g. list of dictionaries.)

## Installation

- Clone the project from GitHub
- Navigate to the project folder, then `poetry install`

## Usage

In IPython or in Jupyter Notebook,

```python
>>> from tinydb_viewer import TinyDBViwer, TinyDB
>>> tdb = TinyDB('db.json')
>>> records = tdb.search(tdb.query['foo'] == 'bar')
>>> viewer = TinyDBViewer(records, sort_func=lambda x: x['baz'])
>>> viewer.view()
'The first page is shown.'
>>> viewer.view(-1)
'The last page is shown.'
>>> viewer.previous()
'The previous page (i-1) is shown.'
>>> viewer.next()
'The next page (i+1) is shown.'
```

## How it works

This works by [the power of pyexcel](https://pyexcel.readthedocs.io/en/latest/design.html#examples-of-supported-data-structure). If you are interested in extending the viewer format, just change the `viewer_func` (which defaults to `lambda x: pyexcel.get_sheet(records=x)`). Some possible extensions are https://github.com/pyexcel/pyexcel#available-plugins

## Bonus

I extended TinyDB a little. My TinyDB is 'ensure_ascii' = False by default, so that the file is a little smaller.

```python
>>> from tinydb_viewer import TinyDBViwer, TinyDB
>>> tdb = TinyDB('db.json')
>>> schema = tdb.schema()
>>> schema
{'_default': {'patho_id': <class 'str'>, 'patient_id': <class 'int'>, 'full_name': <class 'str'>, 'pathologist': <class 'str'>, 'resident': <class 'str'>, 'received': 'datetime str'}}
```

To ensure consistent types:

```python
>>> tdb.insert_multiple(tdb.sanitize_records(records))
```

## Screenshots

![](/screenshots/jupyter0.png?raw=true)
![](/screenshots/jupyter1.png?raw=true)

## Plans

Use [pyhandsontable](https://github.com/patarapolw/pyhandsontable) for the default viewer (which may allows editing of items via webserver's API).
