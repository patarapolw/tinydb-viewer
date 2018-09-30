import pyexcel
import requests

from .config import config


class DataTable:
    def __init__(self, records, table_name, **kwargs):
        renderers = kwargs.pop('renderers', dict())
        web_config = kwargs.pop('config', dict())

        headers = list()
        for record in records:
            for k in record.keys():
                if k not in headers:
                    headers.append(k)

        columns = []
        for header in headers:
            columnData = {
                'data': header
            }
            if header in renderers.keys():
                columnData['renderer'] = renderers.get(header)
            columns.append(columnData)

        web_config.update({
            'colHeaders': headers,
            'rowHeaders': [r.doc_id for r in records],
            'columns': columns,
            'data': records
        })

        self.web_config = web_config
        self.table_name = table_name
        self.records = records

    def _repr_html_(self):
        try:
            url = 'http://{}:{}'.format(config['host'], config['port'])
            r = requests.post('{}/api/create'.format(url), json={
                'tableName': self.table_name,
                'handsontable': self.web_config,
                'fileId': config['file_id']
            })
            r.raise_for_status()
            return '<iframe src="{}" width=800></iframe>'.format(url)
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            return pyexcel.get_sheet(records=self.records).html
