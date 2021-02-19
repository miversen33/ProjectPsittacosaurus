from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from flask import current_app as app

# iterate through the modules in the current package
[
    import_module(f"{__name__}.{module_name}")
    for (_, module_name, _) in iter_modules([Path(__file__).resolve().parent])
]


def check_db():
    # TODO(Mike): This should instead check for if the server is running in development mode instead of
    # looking for the "watch triggers" config. If we are in development mode, it makes sense that
    # we would just auto create any new triggers that are created. However if we aren't in development 
    # (IE, we are in testing/production/etc), we _shouldn't_ do that.
    if app.config.get("WATCH_TRIGGERS", False):
        from database.setup.triggers.create_triggers import check_for_missing_triggers
        check_for_missing_triggers(app.db.engine)

    from database.setup.init_scripts.table_population import populate_tables
    populate_tables()
    pass


if app:
    check_db()