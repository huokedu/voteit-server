from flask import request
from flask.ext.cors import cross_origin

from voteit.core import app, motions, vote_events, issues
from voteit.core import parties, persons
from voteit.util import jsonify, paginate_cursor, obj_or_404
from voteit.stancer import generate_stances
from voteit.validation import validate_issue

from bson.objectid import ObjectId


@app.route('/api/1')
@app.route('/')
@cross_origin(headers=['Content-Type'])
def api_index():
    return jsonify({'status': 'ok'})


@app.route('/api/1/stances')
@cross_origin(headers=['Content-Type'])
def stances_get():
    blocs = request.args.getlist('bloc')
    issue_args = request.args.getlist('issue')
    filters = {}
    for criterion in request.args.getlist('filter'):
        if not ':' in criterion:
            continue
        field, value = criterion.split(':', 1)
        filters[field] = value
    stances = generate_stances(blocs, issue_args, filters)
    data = {
        'request': {
            'blocs': blocs,
            'filters': filters,
            'issues': issue_args
        },
        'stances': stances,
        'num_stances': len(stances)
    }
    return jsonify(data)


@app.route('/api/1/motions')
@cross_origin(headers=['Content-Type'])
def motions_index():
    q = request.args.get('q', '').strip()
    query = {}
    if len(q):
        regex = '.*%s.*' % q
        query = {'$or': [{'text': {'$regex': regex}},
                         {'title': {'$regex': regex}}]}
    cur = motions.find(query, {'vote_events.votes': False})
    data = paginate_cursor(cur)
    return jsonify(data)


@app.route('/api/1/motions/<motion_id>')
@cross_origin(headers=['Content-Type'])
def motions_get(motion_id):
    obj = motions.find_one({'motion_id': motion_id})
    obj = obj_or_404(obj)
    return jsonify(obj)


@app.route('/api/1/vote_events')
@cross_origin(headers=['Content-Type'])
def vote_events_index():
    cur = vote_events.find({}, {'votes': False})
    data = paginate_cursor(cur)
    return jsonify(data)


@app.route('/api/1/vote_events/<identifier>')
@cross_origin(headers=['Content-Type'])
def vote_events_get(identifier):
    obj = vote_events.find_one({'identifier': identifier})
    obj = obj_or_404(obj)
    return jsonify(obj)


@app.route('/api/1/parties')
@cross_origin(headers=['Content-Type'])
def parties_index():
    cur = parties.find({})
    data = paginate_cursor(cur)
    return jsonify(data)


@app.route('/api/1/parties/<path:id>')
@cross_origin(headers=['Content-Type'])
def parties_get(id):
    obj = parties.find_one({'id': id})
    obj = obj_or_404(obj)
    return jsonify(obj)


@app.route('/api/1/persons')
@cross_origin(headers=['Content-Type'])
def persons_index():
    cur = persons.find({})
    data = paginate_cursor(cur)
    return jsonify(data)


@app.route('/api/1/persons/<path:id>')
@cross_origin(headers=['Content-Type'])
def persons_get(id):
    obj = persons.find_one({'id': id})
    obj = obj_or_404(obj)
    return jsonify(obj)


#------
# Issues API
#-------

@app.route('/api/1/issues', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def list_issues():
    cur = issues.find()
    data = paginate_cursor(cur)
    return jsonify(data)


@app.route('/api/1/issues', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def create_issue():
    issue = request.json
    if '_id' in issue:
        del issue['_id']

    validate_issue(issue)

    issue_id = issues.insert(issue)
    issue['_id'] = issue_id
    return jsonify(issue, status=201)


@app.route('/api/1/issues/<string:id>', methods=['DELETE'])
@cross_origin(headers=['Content-Type'], methods=['DELETE', 'PUT', 'GET'])
def delete_issue(id):
    issues.remove(ObjectId(id))
    return '', 204


@app.route('/api/1/issues/<string:id>')
@cross_origin(headers=['Content-Type'])
def get_issue(id):
    issue = issues.find_one({'_id': ObjectId(id)})
    return jsonify(issue)


@app.route('/api/1/issues/<string:id>', methods=['PUT'])
@cross_origin(headers=['Content-Type'])
def update_issue(id):
    issue = request.json
    issue['_id'] = ObjectId(id)

    validate_issue(issue)

    issues.save(issue)
    return jsonify(issue)


