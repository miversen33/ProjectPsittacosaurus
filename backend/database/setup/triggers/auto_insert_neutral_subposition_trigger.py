_function_creation = '''
CREATE FUNCTION auto_insert_neutral_subposition()
RETURNS TRIGGER
AS $$
    INSERT_SUBPOSITION_QUERY = "INSERT INTO subposition (name, parent_position_id) VALUES ('Neutral', $1)"

    plpy.prepare(INSERT_SUBPOSITION_QUERY, ['int']).execute([TD['new']['id']])
$$
LANGUAGE plpython3u
;
'''

_trigger_creation = '''
CREATE TRIGGER "auto_insert_neutral_subposition"
AFTER INSERT ON position
FOR EACH ROW
EXECUTE FUNCTION auto_insert_neutral_subposition()
'''

_trigger_existence = '''
SELECT EXISTS(SELECT oid FROM pg_trigger WHERE tgname = 'auto_insert_neutral_subposition');
'''

_function_existence = '''
SELECT EXISTS(SELECT oid FROM pg_proc WHERE proname = 'auto_insert_neutral_subposition');
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
