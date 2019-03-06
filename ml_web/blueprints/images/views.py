from flask import Blueprint, render_template
from ml_web.util.helper_clarifai import app_clarifai, get_relevant_tags

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():

    result = get_relevant_tags('https://samples.clarifai.com/metro-north.jpg')

    print(result)

    return render_template('images/new.html')


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
