from app import app
from flask import Flask, render_template, blueprints
from flask_assets import Environment, Bundle
from ml_web.util.assets import bundles
from ml_web.blueprints.buyers.views import buyers_blueprint
from ml_web.blueprints.sellers.views import sellers_blueprint
from ml_web.blueprints.images.views import images_blueprint
from ml_web.blueprints.sessions.views import sessions_blueprint
import os
import config

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(buyers_blueprint, url_prefix="/buyers")
app.register_blueprint(sellers_blueprint, url_prefix="/sellers")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
