import os
from datetime import timedelta

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG)

class Config:
    SECRET_KEY = os.getenv('Chave', 'segredo')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://matheus:admin@localhost:5432/saude_df')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_CHAVE_SECRETA', 'segredo-jwt')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)