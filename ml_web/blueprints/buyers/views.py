from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.base_model import db, BaseModel
from models.buyer import Buyer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


buyers_blueprint = Blueprint('buyers',
                            __name__,
                            template_folder='templates')


@buyers_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('buyers/new.html')


@buyers_blueprint.route('/', methods=['POST'])
def create():
   
    user_password = request.form['password']
    hashed_password = generate_password_hash(user_password)

    buyer = Buyer(username=request.form['username'],
                email=request.form['email'], password=hashed_password)

    if buyer.save():
        flash("Successfully registered")
        session['username'] = request.form['username']
        login_user(buyer)
        return redirect(url_for('buyers.index'))
    else:
        return render_template('buyers/new.html', username=request.form['username'], email=request.form['email'], password=request.form['password'], errors=buyer.errors)



@buyers_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@buyers_blueprint.route('/', methods=["GET"])
def index():
    return render_template('buyers/buyer.html')


@buyers_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@buyers_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
