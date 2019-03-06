from flask import Blueprint, render_template
from ml_web.util.helper_clarifai import app_clarifai, get_relevant_tags

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():

    pass


@images_blueprint.route('/', methods=['POST'])
def create():
    pass


@images_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@images_blueprint.route('/', methods=["GET"])
def index():
    return "images"


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@images_blueprint.route('/test_search', methods=['GET'])
def test_search():
    result = get_relevant_tags('https://sanrio-production-weblinc.netdna-ssl.com/media/W1siZiIsIjIwMTYvMDYvMTQvMjAvNDgvMzQvMTM3L2NocmFjdGVyX2hlbGxvX2tpdHR5LmpwZyJdLFsicCIsIm9wdGltIl1d/chracter-hello-kitty.jpg?sha=bb1658addec8d1b7')

    print(result)

    return render_template('images/new.html')