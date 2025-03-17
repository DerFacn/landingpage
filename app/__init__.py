from flask import Flask
from app.config import Config


def create_app(config_obj=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from app.routes import register_functions

    register_functions(app)

    return app
