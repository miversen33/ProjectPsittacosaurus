_function_creation = '''
CREATE FUNCTION auto_insert_attribute_subtables()
RETURNS TRIGGER
AS $$
    ATTRIBUTE_IS_BOOSTABLE_QUERY = 'SELECT boostable FROM attribute WHERE id = $1'
    PLAYER_FETCH_QUERY = 'SELECT id FROM player_info'
    PLAYER_ATTRIBUTE_INSERT_QUERY = 'INSERT INTO player_attribute (player_id, attribute_id, attribute_value) VALUES ($1, $2, 40)'
    PLAYER_ATTRIBUTE_BOOST_INSERT_QUERY = 'INSERT INTO attribute_boost (player_id, attribute_id, ingame_boost, momentum_boost) VALUES ($1, $2, 0, 0)'
    SUBPOSITION_FETCH_QUERY = 'SELECT id, parent_position_id FROM subposition'
    BASE_ATTRIBUTE_INSERT_QUERY = f'INSERT INTO base_attribute (position_id, subposition_id, attribute_id, attribute_value, attribute_deviation, attribute_mean, attribute_generation_cap, attribute_importance) VALUES ($1, $2, $3, $4 , 0.0, $5, $6, .25)'

    attribute_id = TD['new']['id']
    attribute_is_boostable = TD['new']['boostable']
    override_value = TD["new"]["name"].lower() in ["stamina", "injury_resistance"]
    var_4 = 80 if override_value else 40
    var_5 = var_4
    var_6 = 1 if override_value else 5
    for player in plpy.execute(PLAYER_FETCH_QUERY):
        plpy.prepare(PLAYER_ATTRIBUTE_INSERT_QUERY, [
                        "int", "boolean"]).execute([player['id'], true])
        if attribute_is_boostable:
            plpy.prepare(PLAYER_ATTRIBUTE_BOOST_INSERT_QUERY, [
                            "int", "int"]).execute([player["id"], attribute_id])

    for subposition in plpy.execute(SUBPOSITION_FETCH_QUERY):
        plpy.prepare(BASE_ATTRIBUTE_INSERT_QUERY, ["int", "int", "int", "int", "int", "int"]).execute(
            [subposition["parent_position_id"], subposition["id"], attribute_id, var_4, var_5, var_6])
$$
LANGUAGE plpython3u
;
'''

_trigger_creation = '''
CREATE TRIGGER "auto_insert_attribute_subtables"
AFTER INSERT ON attribute
FOR EACH ROW
EXECUTE FUNCTION auto_insert_attribute_subtables()
'''

_trigger_existence = '''
SELECT EXISTS(SELECT oid FROM pg_trigger WHERE tgname = 'auto_insert_attribute_subtables');
'''

_function_existence = '''
SELECT EXISTS(SELECT oid FROM pg_proc WHERE proname = 'auto_insert_attribute_subtables');
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
