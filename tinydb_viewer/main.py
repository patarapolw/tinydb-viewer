import pyexcel


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
