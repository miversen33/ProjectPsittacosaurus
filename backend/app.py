#!/usr/bin/env python

import os
from typing import Any
from json import JSONDecodeError

from flask import Flask, json, request
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    init_app(app)
    return app


def init_app(app):
    load_config(app)
    init_db(app)
    create_routes(app)

    return app


def load_config(app):
    try:
        _config = os.environ.get("CONFIG")
    except KeyError:
        _config = "Development"
        print(
            "Error trying to pull CONFIG from os environment. Defaulting to Development"
        )
    if _config is None:
        print('No config provided. Defaulting to development config')
        _config = 'Development'
    app.config.from_object(f"config.config.{_config}")

    if app.config.get("DATABASE_URI") == "sqlite:///memory" and os.environ.get("DATABASE_URI"):
        print('Received Database URI via environment variable. Overwriting sqlite:///memory')
        app.config['DATABASE_URI'] = os.environ.get("DATABASE_URI")
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URI")
    except Exception as exception:
        print(repr(exception), exception)


def init_db(app):
    app.db = SQLAlchemy(app)
    with app.app_context():
        # import models
        from models.models import init_tables
        init_tables(app.db)
    # app.db.create_all()

    def attempt_commit():
        # from sqlalchemy.exc import InterfaceError
        try:
            app.db.session.commit()
        except Exception as exception:
            app.db.session.rollback()
            raise
    app.db.session.attempt_commit = attempt_commit

    if app.config.get('WATCH_TRIGGERS', False):
        from database.setup.triggers import create_triggers
        create_triggers.check_for_missing_triggers(app.db.engine)
    pass

    # Verify all triggers are present


def get_db():

    pass


def create_routes(app):
    app.route = route
    with app.app_context():
        import controllers

# Overrides the default `app.route` to wrap relevant routes behind a session checker


def route(rule='', **options):
    def _validate_session(f):
        from flask import current_app as app
        from modules.authenticate import validate_session
        from modules.response import Response
        from modules.server_response_statuses import NOT_AUTHORIZED_ERROR

        if 'methods' not in options.keys():
            options['methods'] = ['GET']
        bypass_session_validation = options.pop(
            'bypass_session_validation', False)
        is_internal = options.pop('is_internal', False)
        endpoint = options.pop("endpoint", None)

        def decorator():
            if validate_session():
                response = f()
                # log_api_hit(route, _data.copy(), response)
                return response
            else:
                return Response(status_code=NOT_AUTHORIZED_ERROR, status_text='Invalid Session')

        if not bypass_session_validation and not is_internal:
            decorator.__name__ = f.__name__
            app.add_url_rule(rule=rule, endpoint=endpoint,
                             view_func=decorator, **options)
            return decorator
        else:
            app.add_url_rule(rule=rule, endpoint=endpoint,
                             view_func=f, **options)
            return f
    return _validate_session


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
    )
