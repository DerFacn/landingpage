from flask import Flask
from app.config import Config


def create_app(config_obj=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return {"message": "hello world"}

    return app
