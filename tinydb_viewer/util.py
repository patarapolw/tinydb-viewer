import tinydb


class MyTinyDB(tinydb.TinyDB):
    def __init__(self, *args, **kwargs):
        if 'ensure_ascii' not in kwargs.keys():
            kwargs['ensure_ascii'] = False

        self.query = tinydb.Query()

        super().__init__(*args, **kwargs)
