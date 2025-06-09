import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('Chave', 'segredo')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@localhost/saude_df')
    JWT_SECRET_KEY = os.getenv('JWT_CHAVE_SECRETA', 'segredo-jwt')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)