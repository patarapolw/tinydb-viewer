import pyexcel


class TinyDBViewer:
    def __init__(self, records, chunk_size=10, sort_func=None, viewer_func=None):
        self.viewer_func = viewer_func
        if self.viewer_func is None:
            self.viewer_func = lambda x: pyexcel.get_sheet(records=x)

        self.records = sorted(records, key=sort_func)
        self.i = 0
        self.chunk_size = chunk_size

    def view(self, page_number=None):
        if page_number is None:
            page_number = self.i
        elif page_number == -1:
            page_number = len(self.records) // self.chunk_size

        self.i = page_number

        return self.viewer_func(self.records[page_number * self.chunk_size:
                                             (page_number + 1) * self.chunk_size])

    def next(self):
        if len(self.records) < (self.i + 1) * self.chunk_size:
            self.i = 0
        else:
            self.i += 1

        return self.view()

    def previous(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.records) // self.chunk_size

        return self.view()

    def first(self):
        self.i = 0

        return self.view()

    def last(self):
        self.i = -1

        return self.view()
