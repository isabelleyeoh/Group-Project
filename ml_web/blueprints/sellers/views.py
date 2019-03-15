from flask import Blueprint, render_template
from models.image import Image


sellers_blueprint = Blueprint('sellers',
                            __name__,
                            template_folder='templates')


@sellers_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sellers/seller.html')


@sellers_blueprint.route('/', methods=['POST'])
def create():
    pass


@sellers_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sellers_blueprint.route('/', methods=["GET"])
def index():
    return render_template('sellers/seller.html')


@sellers_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sellers_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@sellers_blueprint.route('/<int:id>', methods=['GET'])
def product(id):
    pass

