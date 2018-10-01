from flask import request, jsonify, Response

from . import app
from .config import config


@app.route('/api/create', methods=['POST'])
def create_table():
    r = request.get_json()
    if r['fileId'] == config['get_file_id']():
        config['table'] = config['tinydb'].table(r['tableName'])
        config['handsontable'].update(r['handsontable'])

        return Response(status=201)
    else:
        return Response(status=304)


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
