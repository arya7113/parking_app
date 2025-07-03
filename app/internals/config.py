class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevlopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'this-is-a-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parkingapp.sqlite3'
    JWT_SECRET_KEY = 'this-is-a-secret'   
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_COOKIE_CSRF_PROTECT = False  # Optional, disable for simplicity in dev

