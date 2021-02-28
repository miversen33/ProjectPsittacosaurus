#!/usr/bin/env python

import os
from typing import Any
import logging

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
    _pending_logs = [{'level': logging.DEBUG, 'log': 'Loading Configuration'}]
    try:
        _config = os.environ.get("CONFIG")
    except KeyError:
        _config = "Development"
        _pending_logs.append({'level': logging.DEBUG, 'log': "Error trying to pull CONFIG from os environment. Defaulting to Development"})
    if _config is None:
        _pending_logs.append({'level': logging.DEBUG, 'log': 'No config provided. Defaulting to development config'})
        _config = 'Development'
    app.config.from_object(f"config.config.{_config}")

    # We need this to be done after the config is loaded
    with app.app_context():
        from modules.logger import init_logger
        init_logger(app, 'server')
        # Im not sold on exactly how to do this since we are going to have to do some fancy shit to make the APILogger be usable with the logger. It might be 
        # worth creating a completely different handler for the API that we init here, but then we still need to figure out how to send all the API info over
        init_logger(app, 'api')

    logger = logging.getLogger('server')
    [logger.log(level=log['level'], msg=log['log']) for log in _pending_logs]
    del _pending_logs

    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URI")
    except Exception as exception:
        logger.log(logging.ERROR, f"No database found. Exception: {exception} -> {repr(exception)}")
    logger.log(logging.DEBUG, 'Configuration Loaded')


def init_db(app):
    logger = logging.getLogger('server')
    logger.log(logging.DEBUG, 'Initializing Database')
    app.db = SQLAlchemy(app)
    def attempt_commit():
        try:
            app.db.session.commit()
        except:
            app.db.session.rollback()
            logging.getLogger('server').log(logging.ERROR, 'Unable to commit database changes!')
            raise
    app.db.session.attempt_commit = attempt_commit
    
    with app.app_context():
        import models
        # While this may seem unimportant, this actually runs models/__init__.py which initializes all the models. Ignore linting errors here
    logger.log(logging.DEBUG, 'Database Initialized')


def create_routes(app):
    logger = logging.getLogger('server')
    logger.log(logging.DEBUG, 'Creating Routes')
    app.route = route
    with app.app_context():
        import controllers
    logger.log(logging.DEBUG, 'Routes Created')

# Overrides the default `app.route` to wrap relevant routes behind a session checker

def route(rule="", **options):
    def _validate_session(f):
        from flask import current_app as app
        from modules.authenticate import validate_session
        from modules.response import Response
        from modules.server_response_statuses import NOT_AUTHORIZED_ERROR

        if "methods" not in options.keys():
            options["methods"] = ["GET"]
        bypass_session_validation = options.pop("bypass_session_validation", False)
        is_internal = options.pop("is_internal", False)
        endpoint = options.pop("endpoint", None)

        def decorator():
            if validate_session():
                response = f()
                # TODO(Mike): Go read APILog.Factory
                # log_api_hit(route, _data.copy(), response)
                return response
            else:
                return Response(
                    status_code=NOT_AUTHORIZED_ERROR, status_text="Invalid Session"
                )

        if not bypass_session_validation and not is_internal:
            decorator.__name__ = f.__name__
            app.add_url_rule(
                rule=rule, endpoint=endpoint, view_func=decorator, **options
            )
            return decorator
        else:
            app.add_url_rule(rule=rule, endpoint=endpoint, view_func=f, **options)
            return f

    return _validate_session


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
    )
