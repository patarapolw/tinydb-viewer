# tinydb-viewer

View records generated from [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) and alike (e.g. list of dictionaries.)

## Installation

- Clone the project from GitHub
- Navigate to the project folder, then `poetry install`

## Usage

In IPython or in Jupyter Notebook,

```python
>>> import tinydb
>>> tdb = tinydb.TinyDB('db.json')
>>> query = tinydb.Query()
>>> records = tdb.search(query['foo'] == 'bar')
>>> from tinydb_viewer import TinyDBViwer
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

## Additional plugins

- [pyhandsontable](https://github.com/patarapolw/pyhandsontable)

## Screenshots

![](/screenshots/jupyter.png?raw=true)
