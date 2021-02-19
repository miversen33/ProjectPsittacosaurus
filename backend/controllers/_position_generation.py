from json import JSONDecodeError
from flask import render_template, request, current_app as app, json
from modules.response import Response
from modules.server_response_statuses import BAD_REQUEST, SUCCESS
from models.position import Position, Subposition

_TEMPLATE = '_position_creation.html'


@app.route('/_position_generation', is_internal=True)
def position_generation_page():
    vars = {}
    return render_template(_TEMPLATE, **vars)


@app.route('/get_positions', is_internal=True)
def get_positions():
    side = request.args.get('side')
    if side is None:
        return Response(data={'message': 'Side was not provided'}, status_code=BAD_REQUEST)
    return json.dumps([position.name for position in Position.query.filter_by(side=side).all()])


@app.route('/get_subpositions', is_internal=True)
def get_subpositions():
    position = request.args.get('position')
    if position is None:
        return Response(data={'message': 'Position was not provided'}, status_code=BAD_REQUEST)

    position_id = Position.query.filter_by(name=position).first()
    if position_id is None:
        return Response(data={'message': 'Invalid Position'}, status_code=BAD_REQUEST)
    position_id = position_id.id
    return json.dumps([position.name for position in Subposition.query.filter_by(parent_position_id=position_id).all()])


@app.route('/save_position', is_internal=True, methods=['POST'])
def save_position():
    data = None
    try:
        data = json.loads(request.data)
    except JSONDecodeError:
        return Response(data={'message': 'No data was provided'}, status_code=BAD_REQUEST)
    if data is None:
        return Response(data={'message': 'No data was provided'}, status_code=BAD_REQUEST)

    position = data.get('position')
    side = data.get('side')
    if position is None:
        return Response(data={'message': 'No position was provided'}, status_code=BAD_REQUEST)

    if side is None:
        return Response(data={'message': 'No side was provided'}, status_code=BAD_REQUEST)

    db = app.db
    if(Position.query.filter(Position.name.ilike('Quarterback')).limit(1).count() > 0):
        return Response(data={'message': f'Position: {position} already exists, unable to add.'}, status_code=SUCCESS)
    db.session.add(Position(name=position, side=side))
    db.session.attempt_commit()
    return Response()


@app.route('/save_subposition', is_internal=True, methods=['POST'])
def save_subposition():
    data = None
    try:
        data = json.loads(request.data)
    except JSONDecodeError:
        return Response(data={'message': 'No data was provided'}, status_code=BAD_REQUEST)

    if data is None:
        return Response(data={'message': 'No data was provided'}, status_code=BAD_REQUEST)

    position = data.get('position')
    subposition = data.get('subposition')
    if position is None:
        return Response(data={'message': 'No position was provided'}, status_code=BAD_REQUEST)

    if subposition is None:
        return Response(data={'message': 'No subposition was provided'}, status_code=BAD_REQUEST)

    db = app.db
    parent_position = Position.query.filter_by(name=position).first()

    if parent_position is None:
        return Response(data={'message': f'Invalid position ({position}) was provided'}, status_code=BAD_REQUEST)

    parent_position = parent_position.id
    db.session.add(Subposition(name=subposition,
                               parent_position_id=parent_position))
    db.session.attempt_commit()
    return Response()
