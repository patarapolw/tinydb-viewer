try:
    from tinydb_constraint import ConstraintTable as Table
except ImportError:
    from tinydb.database import Table

from .renderer import DataTable


class ViewableTable(Table):
    view_dict = None

    def all(self, **kwargs):
        records = super().all()
        self._viewer_init(records, **kwargs)

        return records

    def search(self, cond, **kwargs):
        records = super().search(cond)
        self._viewer_init(records, **kwargs)

        return records

    def _viewer_init(self, records, chunk_size=10, sort_func=None, viewer_func=None, **kwargs):
        if viewer_func is None:
            viewer_func = lambda x: DataTable(x, table_name=self.name, **kwargs)

        if not sort_func:
            sort_func = lambda x: -getattr(x, 'doc_id', 0)

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
