# TODO(Mike): Test me
_function_creation = '''
CREATE FUNCTION auto_insert_attribute_for_subpositions()
RETURNS TRIGGER
AS $$
    ATTRIBUTE_FETCH_QUERY = 'SELECT id FROM attribute'
    BASE_ATTRIBUTE_INSERT_QUERY = 'INSERT INTO base_attribute (position_id, subposition_id, attribute_id, attribute_value, attribute_deviation, attribute_mean, attribute_generation_cap, attribute_importance) VALUES ($1, $2, $3, 40.0, 0.0, 40.0, 5.0, .25)'

    subposition_id = TD['new']['id']
    position_id = TD['new']['parent_position_id']
    for attribute in plpy.execute(ATTRIBUTE_FETCH_QUERY):
        plpy.prepare(BASE_ATTRIBUTE_INSERT_QUERY, ["int", "int", "int"]).execute([position_id, subposition_id, attribute.get('id')])
$$
LANGUAGE plpython3u
;
'''

_trigger_creation = '''
CREATE TRIGGER "auto_insert_attribute_for_subpositions"
AFTER INSERT ON subposition
FOR EACH ROW
EXECUTE FUNCTION auto_insert_attribute_for_subpositions()
'''

_trigger_existence = '''
SELECT EXISTS(SELECT oid FROM pg_trigger WHERE tgname = 'auto_insert_attribute_for_subpositions');
'''

_function_existence = '''
SELECT EXISTS(SELECT oid FROM pg_proc WHERE proname = 'auto_insert_attribute_for_subpositions');
'''


def create(db):
    create_function(db)
    create_trigger(db)


def _does_trigger_exist(db) -> bool:
    return db.execute(_trigger_existence).first()[0]


def _does_function_exist(db) -> bool:
    return db.execute(_function_existence).first()[0]


def create_function(db):
    if _does_function_exist(db):
        return

    db.execute(_function_creation)


def create_trigger(db):
    if _does_trigger_exist(db):
        return
    db.execute(_trigger_creation)
