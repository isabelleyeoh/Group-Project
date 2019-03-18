from flask import Blueprint, render_template
from models.image import Image
from models.product import Product
from models.user import User
from flask_login import login_required


sellers_blueprint = Blueprint('sellers',
                            __name__,
                            template_folder='templates')


@sellers_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('sellers/seller.html')


@sellers_blueprint.route('/<int:id>', methods=["GET"])
@login_required
def show(id):
    products=Product.select().where(Product.seller_id==id)
    user=User.get_by_id(id)
    return render_template('sellers/database.html', products=products, user=user)


@sellers_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('sellers/seller.html')


