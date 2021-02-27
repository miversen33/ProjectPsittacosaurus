import logging
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
                logging.getLogger('server').log(logging.INFO, f'I dont know what you want me to do with state: {state}')
        except Exception as exception:
            status = 500
            logging.getLogger('server').log(logging.INFO, f'Received exception while trying to save attribute {name}. Error: {exception} -> {repr(exception)}')
            message = repr(exception)

    return json.dumps(dict(status=status, message=message))


def _remove_attribute(name):
    name = name.lower().replace(' ', '_')
    db = app.db
    attribute = Attribute.query.filter_by(name=name).first()
    if attribute:
        db.session.delete(attribute)
        logging.getLogger('server').log(logging.DEBUG, f'Removing Attribute: {repr(attribute)}')
        db.session.attempt_commit()


def _save_attribute(name, boostable):
    db = app.db
    name = name.lower().replace(' ', '_')
    attributes = Attribute.query.filter(Attribute.name == name)
    if len(attributes.all()) > 0:
        logging.getLogger('server').log(logging.DEBUG, f'Updating Attribute: {name} to Boostable Value: {boostable}')
        attributes.update({'boostable': boostable})
    else:
        attribute = Attribute(name=name, boostable=boostable)
        logging.getLogger('server').log(logging.DEBUG, f'Adding Attribute: {repr(attribute)}')
        db.session.add(attribute)
    db.session.attempt_commit()
