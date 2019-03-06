from flask import Blueprint, render_template


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    pass


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return "sessions"


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
