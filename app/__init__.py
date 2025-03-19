from flask import Flask
from app.config import Config
from alchemical.flask import Alchemical

db = Alchemical(session_options={'expire_on_commit': False})


def create_app(config_obj=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)

    from app import models
    from app.routes import register_functions

    register_functions(app)

    with app.app_context():
        db.create_all()

    return app
