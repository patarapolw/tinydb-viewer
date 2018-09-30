from tinydb.database import Table
import dateutil.parser

from .util import remove_control_chars
from .config import config
from .renderer import DataTable


class ViewableTable(Table):
    view_dict = None

    def insert(self, element, sanitize=True):
        if sanitize:
            return super().insert(self.sanitize_records([element])[0])
        else:
            return super().insert(element)

    def insert_multiple(self, elements, sanitize=True):
        if sanitize:
            return super().insert_multiple(self.sanitize_records(elements))
        else:
            return super().insert_multiple(elements)

    def update(self, fields, sanitize=True, cond=None, doc_ids=None, eids=None):
        if sanitize:
            if callable(fields):
                _update = lambda data, eid: self.sanitize_records([fields(data[eid])])[0]
            else:
                _update = lambda data, eid: data[eid].update(self.sanitize_records([fields])[0])

            self.process_elements(_update, cond, eids)
        else:
            super().update(fields, sanitize=True, cond=None, doc_ids=None, eids=None)

    def sanitize_records(self, records):
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

                table_schema.update(self._record_schema(record, show_datetime=False))

                yield record

        table_schema = self.schema()
        for v in table_schema.values():
            assert not isinstance(v, (list, tuple, set))

        return list(_records())

    def schema(self):
        result = dict()

        for record in self.all():
            for k, v in self._record_schema(record).items():
                result.setdefault(k, set()).add(v)

        for k, v in result.items():
            if len(v) == 1:
                result[k] = v.pop()
            else:
                result[k] = list(v)

        return result

    @staticmethod
    def _record_schema(record, show_datetime=None):
        if show_datetime is None:
            show_datetime = config['show_datetime']

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

    def all(self, *args, **kwargs):
        records = super().all()
        self._viewer_init(records, *args, **kwargs)

        return records

    def search(self, cond, *args, **kwargs):
        records = super().search(cond)
        self._viewer_init(records, *args, **kwargs)

        return records

    def _viewer_init(self, records, chunk_size=10, sort_func=None, viewer_func=None, viewer_kwargs=None):
        if viewer_func is None:
            if viewer_kwargs is None:
                viewer_kwargs = dict()

            viewer_func = lambda x: DataTable(x, table_name=self.name, **viewer_kwargs)

        if sort_func:
            records = sorted(records, key=sort_func)
        self.view_dict = {
            'func': viewer_func,
            'records': records,
            'i': 0,
            'chuck_size': chunk_size
        }

    def view(self, page_number=None, start=None):
        """Choose a page number to view

        Keyword Arguments:
            page_number {int >= -1} -- Page number to view (default: {self.i})
            start {int} -- Sequence of the record to start viewing (default: {None})

        Returns:
            Viewer function object
        """

        if self.view_dict:
            if page_number is None:
                page_number = self.view_dict['i']
            elif page_number == -1:
                page_number = len(self.view_dict['records']) // self.view_dict['chuck_size']

            self.view_dict['i'] = page_number

            if start is None:
                start = page_number * self.view_dict['chuck_size']

            return self.view_dict['func'](self.view_dict['records'][start: start + self.view_dict['chuck_size']])
        else:
            return 'Please search() first.'

    def next(self):
        """Shows the next page

        Returns:
            Viewer function object
        """

        if self.view_dict:
            if len(self.view_dict['records']) < (self.view_dict['i'] + 1) * self.view_dict['chuck_size']:
                self.view_dict['i'] = 0
            else:
                self.view_dict['i'] += 1

            return self.view()
        else:
            return 'Please search() first.'

    def previous(self):
        """Show the previous page

        Returns:
            Viewer function object
        """

        if self.view_dict:
            self.view_dict['i'] -= 1
            if self.view_dict['i'] < 0:
                self.view_dict['i'] = len(self.view_dict['records']) // self.view_dict['chuck_size']

            return self.view()
        else:
            return 'Please search() first.'

    def first(self):
        """Shows the first page

        Returns:
            Viewer function object
        """

        return self.view(0)

    def last(self):
        """Shows the last page

        Returns:
            Viewer function object
        """

        return self.view(-1)
