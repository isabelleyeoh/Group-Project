from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.base_model import db, BaseModel
from models.buyer import Buyer
from models.seller import Seller
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from ml_web import oauth



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def option():
    return render_template('sessions/option.html')


@sessions_blueprint.route('/new/usertype', methods=['POST'])
def new():        
    usertype = request.form['usertype']
    return redirect(url_for('sessions.usertype', usertype=usertype))


@sessions_blueprint.route('/usertype/<usertype>', methods=['GET'])
def usertype(usertype):        
    return render_template('sessions/new.html', usertype=usertype)


@sessions_blueprint.route('/<usertype>', methods=['POST'])
def create(usertype):
    # userType = int(request.form['userType'])
    usertype = usertype
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    
    # if userType == 1:
    if usertype == 'buyer':
        buyer = Buyer(username=username, email=email, password=hashed_password)
        buyer.save()
        flash("buyer registered")
        user = buyer
        login_user(user)
        return render_template('home.html')

    # elif userType == 2:
    if usertype == 'seller':
        seller = Seller(username=username, email=email, password=hashed_password)
        seller.save()
        flash("seller registered")
        user = seller
        login_seller(seller)
        return render_template('home.html')


@sessions_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/', methods=['POST'])
def check():
    email_to_check = request.form['email']
    password_to_check = request.form['password']
    user = Buyer.get_or_none(Buyer.email == email_to_check) or Seller.get_or_none(Seller.email == email_to_check)
    hashed_password = user.password
    result = check_password_hash(hashed_password, password_to_check)

    if result:
        login_user(user)
        return render_template('home.html')
    else:
        flash("Wrong password")
        return 'logged in failed'


@sessions_blueprint.route('/signin/google', methods=['GET'])
def google_form():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = Buyer.get_or_none(Buyer.email == email) or Seller.get_or_none(Seller.email == email) 

    if user:
        login_user(buyer) or login_user(seller)
        return redirect(url_for('home'))
    else:
        flash('Authentication failed.')
        return redirect(url_for('sessions.login'))


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out")
    return redirect(url_for('sessions.login'))

