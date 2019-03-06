from flask import Blueprint, render_template
from ml_web.util.helper_clarifai import app_clarifai, predict_image_celebrity



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
def predict_celebrity():

    model='celeb-v1.3'
    image='https://akns-images.eonline.com/eol_images/Entire_Site/2018729/rs_1024x759-180829091909-1024-Kirk-Douglas-JR-082918.jpg?fit=inside|900:auto&output-quality=90'
    result = predict_image_celebrity(image=image, model=model)

    print(result)

    return render_template('images/new.html')