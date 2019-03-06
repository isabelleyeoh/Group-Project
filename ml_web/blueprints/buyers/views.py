from flask import Blueprint, render_template


buyers_blueprint = Blueprint('buyers',
                            __name__,
                            template_folder='templates')


@buyers_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('buyers/new.html')


@buyers_blueprint.route('/', methods=['POST'])
def create():
    pass


@buyers_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@buyers_blueprint.route('/', methods=["GET"])
def index():
    return "buyers"


@buyers_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@buyers_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
