from __future__ import annotations

from flask import Flask

from app.extensions import db
from config import Config, get_config


def create_app(config: Config | None = None) -> Flask:
    if config is None:
        config = get_config()

    app = Flask(__name__, template_folder="templates")
    _load_config(app, config)
    _init_extensions(app)
    _register_blueprints(app)

    return app


def _load_config(app: Flask, config: Config) -> None:
    for key, value in vars(config).items():
        if key.isupper():
            app.config[key] = value


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()


def _register_blueprints(app: Flask) -> None:
    from app.api import api_bp, errors_bp
    from app.web import web_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
