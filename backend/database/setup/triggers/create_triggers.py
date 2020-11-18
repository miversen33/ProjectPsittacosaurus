from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
# Use this for debugging/dev purposes only as this will absolutely introduce a performance hit


def check_for_missing_triggers(db):
    for (_, module_name, _) in iter_modules([Path(__file__).resolve().parent]):
        module = f'{__package__}.{module_name}'
        if module.endswith(__name__.split(__package__)[-1].replace('.', '')):
            continue
        trigger_handler = import_module(module)
        if trigger_handler:
            trigger_handler.create(db)
