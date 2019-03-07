import os
import config
from flask import Flask
from models.base_model import db


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'ml_web')

app = Flask('MACHINE LEARNING', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# @app.route('/')
# def index():
    
#     return "Pass"

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

