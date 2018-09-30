import tinydb
import dateutil.parser
import re

all_chars = (chr(i) for i in range(0x110000))
control_chars = ''.join(map(chr, set(range(0, 32)) | set(range(127, 160))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s):
    return control_char_re.sub('', s)


class TinyDB(tinydb.TinyDB):
    def __init__(self, *args, **kwargs):
        if 'ensure_ascii' not in kwargs.keys():
            kwargs['ensure_ascii'] = False

        self.query = tinydb.Query()

        super().__init__(*args, **kwargs)

    def schema(self, table_name=None, parse_datetime=True, dateutil_kwargs=None):
        if dateutil_kwargs is None:
            dateutil_kwargs = dict()

        if table_name:
            tdb = self.table(table_name)
        else:
            tdb = self

        result = dict()

        for record in tdb.all():
            for k, v in _yield_schema(record, parse_datetime, **dateutil_kwargs).items():
                result.setdefault(k, set()).add(v)

        for k, v in result.items():
            if len(v) == 1:
                result[k] = v.pop()
            else:
                result[k] = list(v)

        return result


def _yield_schema(record, parse_datetime, **dateutil_kwargs):
    for k, v in record.items():
        if parse_datetime and isinstance(v, str):
            try:
                dateutil.parser.parse(v, **dateutil_kwargs)
                record[k] = 'datetime'
            except ValueError:
                record[k] = type(v)
        else:
            record[k] = type(v)

    return record


def sanitize_records(records):
    schema = dict()

    for record in records:
        for k, v in record.items():
            if isinstance(v, str):
                v = v.strip()
                if v.isdigit():
                    record[k] = int(v)
                elif '.' in v and v.replace('.', '', count=1).isdigit():
                    record[k] = float(v)
                else:
                    record[k] = v

            type_ = schema.get(k, None)
            if type_:
                assert type_ == type(record[k])

            schema.setdefault(k, type(record[k]))

        yield record
