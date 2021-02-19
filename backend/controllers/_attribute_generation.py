from flask import render_template, request, current_app as app, session, json
from models.attributes import Attribute

_TEMPLATE = '_attribute_generation.html'
_ATTR_NAME = 'attrName'
_BOOSTABLE = 'boostable'
_STATE = 'state'

@app.route('/_attribute_generation', is_internal=True)
def attribute_generation_page():
    vars = dict(
        attrName=_ATTR_NAME,
        boostable=_BOOSTABLE,
        state=_STATE,
        attributes=_get_attributes()
    )
    return render_template(_TEMPLATE, **vars)


def _get_attributes():
    db = app.db
    return [
        dict(
            name=attribute.name.replace('_', ' ').title(),
            boostable=attribute.boostable,
            id=attribute.id
        ) for attribute in Attribute.query
        .order_by(Attribute.name)
        .all()
    ]


@app.route('/_attribute_generation_save_attribute', methods=['POST'], is_internal=True)
def save_attributes():
    data = json.loads(request.data)
    status = 200
    message = ''
    for attr in data:
        name = attr[_ATTR_NAME]
        boostable = attr[_BOOSTABLE]
        state = attr[_STATE]
        try:
            if state == 'removeAttr':
                _remove_attribute(name)
            elif state in ['newAttr', 'modifiedAttr']:
                _save_attribute(name, boostable)
            else:
                print(
                    f'I dont know what you want me to do with state: {state}')
        except Exception as exception:
            status = 500
            message = repr(exception)

    return json.dumps(dict(status=status, message=message))


def _remove_attribute(name):
    name = name.lower().replace(' ', '_')
    db = app.db
    attribute = Attribute.query.filter_by(name=name).first()
    if attribute:
        db.session.delete(attribute)
        db.session.attempt_commit()
    # db.session.delete()


def _save_attribute(name, boostable):
    db = app.db
    name = name.lower().replace(' ', '_')
    attribute = Attribute.query.filter_by(name=name)
    if len(attribute.all()) > 0:
        attribute.update({'boostable': boostable})
    else:
        db.session.add(Attribute(name=name, boostable=boostable))
    db.session.attempt_commit()
