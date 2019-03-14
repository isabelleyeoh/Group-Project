from flask import jsonify, Blueprint, request, make_response
from models.buyer import Buyer
from werkzeug.security import check_password_hash
# from flask_wtf.csrf import CsrfProtect
from ml_web import csrf
from flask_login import login_user

sessions_api_blueprint = Blueprint('sessions_api', __name__)

@sessions_api_blueprint.route('/login', methods=['POST'])
@csrf.exempt
def sign_in():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = Buyer.get_or_none(email=post_data.get('email'))
    if user :
        login_user(user)
        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.'
        }
        return make_response(jsonify(responseObject)), 201

    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return make_response(jsonify(responseObject)), 401
