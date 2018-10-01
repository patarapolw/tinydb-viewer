import tinydb

from . import app
from .table import ViewableTable
from .config import config
from .util import get_file_id


class TinyDB(tinydb.TinyDB):
    def __init__(self, db_path, server_kwargs=None,
                 show_datetime=True,
                 *args, **kwargs):
        """Modifies TinyDB by
        kwargs.setdefault('ensure_ascii', False)
        
        Arguments:
            db_path {str} -- Path to JSON database
            server_kwargs {dict} -- dict to pass to app.run()
        
        Keyword Arguments:
            parse_datetime {bool} -- Whether to not to try parsing datetime from string (default: {True})
            dateutil_kwargs {dict} -- kwargs to pass to dateutil.parser.parse() (default: {dict()})
        """

        if server_kwargs is None:
            server_kwargs = dict()

        kwargs.setdefault('ensure_ascii', False)

        self.query = tinydb.Query()
        config.update({
            'tinydb': self,
            'query': self.query,
            'show_datetime': show_datetime,
            'get_file_id': lambda: get_file_id(db_path),
            **server_kwargs
        })

        self.table_class = ViewableTable
        super().__init__(db_path, *args, **kwargs)

    @classmethod
    def runserver(cls):
        app.run(
            host=config['host'],
            port=config['port'],
            debug=config['debug']
        )
