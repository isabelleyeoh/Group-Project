
from app import app
from flask import Flask, render_template, blueprints, url_for
from flask_assets import Environment, Bundle
from ml_web.util.assets import bundles
import os
import config
from ml_web.helpers.google_oauth import oauth
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.buyer import Buyer
from models.seller import Seller


oauth.init_app(app)

csrf = CSRFProtect(app)

assets = Environment(app)
assets.register(bundles)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    user = Buyer.get_or_none(
        id=user_id) or Seller.get_or_none(id=user_id)
    return user

# @login_manager.user_loader
# def load_user(user_id):
#     return Buyer.get_or_none(id=user_id)

# @login_manager.user_loader
# def load_user(user_id):
#     return Seller.get_or_none(id=user_id)

from ml_web.blueprints.sessions.views import sessions_blueprint
from ml_web.blueprints.buyers.views import buyers_blueprint
from ml_web.blueprints.sellers.views import sellers_blueprint
from ml_web.blueprints.images.views import images_blueprint
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
