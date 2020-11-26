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
    from database.setup.triggers.create_triggers import check_for_missing_triggers

    check_for_missing_triggers(app.db.engine)
    # TODO(Mike): Handle basic setup? Mass insert of starter attributes, positions, subpositions, etc
    pass


if app and app.config.get("WATCH_TRIGGERS", False):
    check_db()