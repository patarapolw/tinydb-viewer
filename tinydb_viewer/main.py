import pyexcel
import tinydb
import dateutil.parser

from .util import remove_control_chars


class TinyDBViewer:
    def __init__(self, records, chunk_size=10, sort_func=None, viewer_func=None):
        """An object to view TinyDB records
        
        Arguments:
            records {iterable} -- Iterable of TinyDB records
        
        Keyword Arguments:
            chunk_size {int} -- Chunk size to view in a table at once (default: {10})
            sort_func {function} -- Function to sort the query (default: {None})
            viewer_func {function} -- 
                Function to view the record 
                (default: {lambda x: pyexcel.get_sheet(records=x)})
        """

        self.viewer_func = viewer_func
        if self.viewer_func is None:
            self.viewer_func = lambda x: pyexcel.get_sheet(records=x)

        self.records = sorted(records, key=sort_func)
        self.i = 0
        self.chunk_size = chunk_size
    
    def __repr__(self):
        return repr(self.view())
    
    def _repr_html_(self):
        return self.view()

    def view(self, page_number=None, start=None):
        """Choose a page number to view
        
        Keyword Arguments:
            page_number {int >= -1} -- Page number to view (default: {self.i})
            start {int} -- Sequence of the record to start viewing (default: {None})
        
        Returns:
            Viewer function object
        """

        if page_number is None:
            page_number = self.i
        elif page_number == -1:
            page_number = len(self.records) // self.chunk_size

        self.i = page_number

        if start is None:
            start = page_number * self.chunk_size

        return self.viewer_func(self.records[start: start + self.chunk_size])

    def next(self):
        """Shows the next page
        
        Returns:
            Viewer function object
        """

        if len(self.records) < (self.i + 1) * self.chunk_size:
            self.i = 0
        else:
            self.i += 1

        return self.view()

    def previous(self):
        """Show the previous page
        
        Returns:
            Viewer function object
        """

        self.i -= 1
        if self.i < 0:
            self.i = len(self.records) // self.chunk_size

        return self.view()

    def first(self):
        """Shows the first page
        
        Returns:
            Viewer function object
        """

        self.i = 0

        return self.view()

    def last(self):
        """Shows the last page
        
        Returns:
            Viewer function object
        """

        self.i = -1

        return self.view()


class TinyDB(tinydb.TinyDB):
    def __init__(self, db_path, *args, **kwargs):
        """Modifies TinyDB by
        kwargs.setdefault('ensure_ascii', False)
        
        Arguments:
            db_path {str} -- Path to JSON database
        
        Keyword Arguments:
            parse_datetime {bool} -- Whether to not to try parsing datetime from string (default: {True})
            dateutil_kwargs {dict} -- kwargs to pass to dateutil.parser.parse() (default: {dict()})
        """

        kwargs.setdefault('ensure_ascii', False)

        self.query = tinydb.Query()

        super().__init__(db_path, *args, **kwargs)

    def schema(self, show_datetime=True):
        """View table's schema

        Returns:
            dict -- Representation of the schema
        """

        def _table_schema(_table_name):
            result = dict()

            for record in self.table(_table_name).all():
                for k, v in self._record_schema(record, show_datetime=show_datetime).items():
                    result.setdefault(k, set()).add(v)

            for k, v in result.items():
                if len(v) == 1:
                    result[k] = v.pop()
                else:
                    result[k] = list(v)

            return result

        all_schemas = dict()

        for table_name in self.tables():
            all_schemas[table_name] = _table_schema(table_name)

        return all_schemas

    def sanitize_records(self, records, table_name=None):
        """Sanitizes records, e.g. from Excel spreadsheet

        Arguments:
            records {iterable} -- Iterable of records

        Keyword Arguments:
            schema {dict} -- Dictionary of schemas (default: {None})
            table_name {str} -- Table name to get from schema (default: {None})

        Returns:
            list -- List of records
        """

        def _records():
            for record in records:
                to_pop = set()

                for k0, v0 in record.items():
                    if isinstance(v0, str):
                        v0 = remove_control_chars(v0.strip())
                        if v0.isdigit():
                            record[k0] = int(v0)
                        elif '.' in v0 and v0.replace('.', '', 1).isdigit():
                            record[k0] = float(v0)
                        elif v0 in {'', '-'}:
                            to_pop.add(k0)
                            continue
                        else:
                            record[k0] = v0

                    type_ = table_schema.get(k0, None)
                    if type_:
                        assert isinstance(type_, type)
                        assert isinstance(record[k0], type_)

                for k0 in to_pop:
                    record.pop(k0)

                table_schema.update(self._record_schema(record))

                yield record

        if table_name is None:
            table_name = '_default'

        table_schema = self.schema().get(table_name, dict())

        for v in table_schema.values():
            assert not isinstance(v, (list, tuple, set))

        return list(_records())

    @staticmethod
    def _record_schema(record, show_datetime=False):
        record = record.copy()

        for k, v in record.items():
            if show_datetime:
                if isinstance(v, str):
                    try:
                        dateutil.parser.parse(v)
                        record[k] = 'datetime str'
                    except ValueError:
                        record[k] = type(v)
                else:
                    record[k] = type(v)
            else:
                record[k] = type(v)

        return record
