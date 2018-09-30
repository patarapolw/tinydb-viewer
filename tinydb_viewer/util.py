import tinydb
import dateutil.parser
import unicodedata, re

all_chars = (chr(i) for i in range(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in {'Cc'})

control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s):
    return unicodedata.normalize("NFKD",
                                 control_char_re.sub('', s))


class TinyDB(tinydb.TinyDB):
    def __init__(self, *args, **kwargs):
        """Modifies tinydb.TinyDB by checking 'ensure_ascii' = False
        """

        if 'ensure_ascii' not in kwargs.keys():
            kwargs['ensure_ascii'] = False

        self.query = tinydb.Query()

        super().__init__(*args, **kwargs)

    def schema(self, parse_datetime=True, dateutil_kwargs=None):
        """View table's schema
        
        Keyword Arguments:
            parse_datetime {bool} -- Whether to not to try parsing datetime from string (default: {True})
            dateutil_kwargs {dict} -- kwargs to pass to dateutil.parser.parse() (default: {dict()})
        
        Returns:
            [type] -- [description]
        """

        def _table_schema(_table_name):
            result = dict()

            for record in self.table(_table_name).all():
                for k, v in record_schema(record, parse_datetime, dateutil_kwargs).items():
                    result.setdefault(k, set()).add(v)

            for k, v in result.items():
                if len(v) == 1:
                    result[k] = v.pop()
                else:
                    result[k] = list(v)

            return result

        if dateutil_kwargs is None:
            dateutil_kwargs = dict()

        all_schemas = dict()
        
        for table_name in self.tables():
            all_schemas[table_name] = _table_schema(table_name)
        
        return all_schemas


def sanitize_records(records, schema=None, table_name=None,
                     parse_datetime=True, dateutil_kwargs=None):
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

            for k, v in record.items():
                if isinstance(v, str):
                    v = remove_control_chars(v.strip())
                    if v.isdigit():
                        record[k] = int(v)
                    elif '.' in v and v.replace('.', '', 1).isdigit():
                        record[k] = float(v)
                    elif v in {'', '-'}:
                        to_pop.add(k)
                        continue
                    else:
                        record[k] = v

                type_ = table_schema.get(k, None)
                if type_:
                    assert isinstance(record[k], type_)

            for k in to_pop:
                record.pop(k)

            table_schema.update(record_schema(record, parse_datetime, dateutil_kwargs))

            yield record

    if schema is None:
        schema = dict()
    
    if table_name is None:
        table_name = '_default'
    
    table_schema = schema.get(table_name, dict())

    for v in table_schema.values():
        assert not isinstance(v, (list, tuple, set))

    return list(_records())


def record_schema(record, parse_datetime=True, dateutil_kwargs=None):
    """Get the schema of a single record
    
    Arguments:
        record {TinyDB record, dict} -- The record to parse
        parse_datetime {bool} -- Whether to not to try parsing datetime from string (default: {True})
        dateutil_kwargs {dict} -- kwargs to pass to dateutil.parser.parse() (default: {dict()})
    
    Returns:
        dict -- Schema of a single record
    """
    record = record.copy()

    if dateutil_kwargs is None:
        dateutil_kwargs = dict()

    for k, v in record.items():
        if parse_datetime and isinstance(v, str):
            try:
                dateutil.parser.parse(v, **dateutil_kwargs)
                record[k] = DateTimeStr
            except ValueError:
                record[k] = type(v)
        else:
            record[k] = type(v)

    return record


class DateTimeStr:
    pass
