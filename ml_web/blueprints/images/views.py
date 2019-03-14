from flask import Blueprint, render_template, request
from ml_web.helpers.helper_clarifai import app_clarifai, model_prediction
from models.image import Image
from models.product import Product

# JM added
from ml_web.helpers.helper_aws import upload_file_to_s3, allowed_file
from werkzeug import secure_filename
from app import app

from PIL import Image as PILImage
from io import BytesIO



images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

# Upload new image
@images_blueprint.route('/new', methods=['GET'])
def new():

    return render_template('images/uploader.html')


@images_blueprint.route('/', methods=['POST'])
def create():
    
    pass


@images_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@images_blueprint.route('/', methods=["GET"])
def index():
    pass


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
