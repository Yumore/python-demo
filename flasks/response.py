from flask import jsonify, Response

from index import app


@app.route('/json')
def json_response():
    data = {'key': 'value'}
    return jsonify(data)


@app.route('/custom')
def custom_response():
    response = Response('Custom response with headers', status=200)
    response.headers['X-Custom-Header'] = 'Value'
    return response
