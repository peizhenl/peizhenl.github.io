import os


class Config(object):
    """base config"""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 9000
    DB_USERNAME = 'root'
    DB_PASSWORD = 'solstice'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'db_gift_store'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
        DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Set the secret key to some random bytes. to encrypy the sessionkey
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key'
    SECRET_KEY = os.urandom(24)
    # whether it automatically reload template
    TEMPLATE_AUTO_RELOAD = True
    # the root path image uploaded
    UPLOAD_AVATAR_FOLDER = "/static/img/avatars"
    UPLOAD_GOODS_FOLDER = "/static/img/goods"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass


config = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig,
    'default': DevConfig
}
