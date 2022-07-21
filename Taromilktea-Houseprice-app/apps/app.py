from flask import Flask
from apps.router import bp
from apps.config import config
from apps.db import db
from apps.common import load_filters
from flask.json import JSONEncoder as _JSONEncoder
import datetime
import uuid
import decimal

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, bytes):
            return o.decode("utf-8")
        raise ServerError()

def add_views(app):
    app.register_blueprint(bp)

def create_app():
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(config['dev'])
    add_views(app)
    app.json_encoder = JSONEncoder

    env = app.jinja_env
    load_filters(env)

    db.init_app(app)
    return app
