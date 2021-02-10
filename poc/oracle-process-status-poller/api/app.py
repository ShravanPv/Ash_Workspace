from logging import getLogger
from logging.config import dictConfig

from flask import Flask, g

import config
from api.db import Session
from api.endpoints import create_restful_api


def create_app():
    app = Flask(config.FLASK_APP_NAME)
    app.config.from_object(config)
    dictConfig(config.LOGGING_CONFIG)
    app.logger.addHandler(getLogger('api'))
    create_restful_api(app)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        if hasattr(g, 'session'):
            g.session.close()
            delattr(g, 'session')
        Session.remove()

    return app
