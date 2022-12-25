import os


class Config(object):
    """Класс конфигурации приложения."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    LENGTH_SHORT_ID = 6