from flask import Flask
from .config import Config
from .extensions import db, jwt

def criar_aplicacao(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # inicializar as extensoes:
    db.init.app(app)
    jwt.init_app(app)

    return app