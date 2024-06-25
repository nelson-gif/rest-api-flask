from flask import Config

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:admin@localhost/inventory_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
