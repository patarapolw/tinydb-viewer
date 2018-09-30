from flask import request, jsonify, Response

from . import app
from .config import config


@app.route('/api/create', methods=['POST'])
def create_table():
    r = request.get_json()
    assert r['fileId'] == config['file_id']

    config.update({
        'table': config['tinydb'].table(r['tableName']),
        'handsontable': r['handsontable']
    })

    return Response(status=201)


@app.route('/api/edit', methods=['POST'])
def edit_record():
    record = request.get_json()
    record_id = config['table'].update({
        record['fieldName']: record['data']
    }, config['query'].id == record['id'])
    record = config['table'].get(record_id)

    return jsonify({
        'id': record_id,
        'record': record
    }), 201


@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = config['table'].get(record_id)
    config['table'].remove(doc_ids=[record_id])

    return jsonify({
        'id': record_id,
        'record': record
    }), 303
