import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    CLARIFAI_API_KEY = os.environ.get('CLARIFAI_API_KEY')
    CLARIFAI_API_KEY_SEARCH = os.environ.get('CLARIFAI_API_KEY_SEARCH')  #Test
    CLARIFAI_APP_ID = os.environ.get('CLARIFAI_APP_ID')
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    # JM added: AWS S3 configuration
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000