class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:12345678@db-dev.c2w11tiph4ya.ap-northeast-2.rds.amazonaws.com:5432/test'
    SECRET_KEY = "LALAVLA"

    MONGODB_DBNAME = 'test'
    MONGODB_HOST = 'ec2-13-125-241-234.ap-northeast-2.compute.amazonaws.com'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'test'
    MONGODB_PASSWORD = '12345678'


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root1592@api-dev-rds.c2w11tiph4ya.ap-northeast-2.rds.amazonaws.com:5432/test'
    SECRET_KEY = "key"

    MONGODB_DBNAME = 'test'
    MONGODB_HOST = 'ec2-13-125-217-177.ap-northeast-2.compute.amazonaws.com'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'test'
    MONGODB_PASSWORD = 'test27017'


def get_config(is_test=True):
    return TestConfig if is_test else ProductConfig
