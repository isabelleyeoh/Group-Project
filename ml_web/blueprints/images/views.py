from flask import Blueprint, render_template, redirect, url_for, request, flash
# from ml_web.util.helper_clarifai import app_clarifai, predict_model_chair
from models.image import Image
from ml_web.helpers.aws_image import upload_file_to_s3, allowed_file
from werkzeug import secure_filename
from app import app
from models.product import Product
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

# Upload new image
@images_blueprint.route('/new', methods=['GET'])
def new():

    return render_template('images/uploader.html')


@images_blueprint.route('/', methods=['POST'])
def create():

    # user = User.get_by_id(id)

    # we check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it's not there, we return an error message
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    # if the key is in the object, we save it in a variable called file.
    file = request.files["user_file"]

    # we check the filename attribute on the object and if it's empty it means the user sumbmitted an empty form, so we return an error message.
    if file.filename == "":
        return "Please select a file"

    # Finally we check that there is a file and that it has an allowed file type(this is what the allowed_file function does, you can check it out in the flask docs).

    if file and allowed_file(file.filename):

        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        custom_concept = request.form['custom_concept']


        product = Product.create(product_url=str(output), name=name, description=description, category=category, price=price, custom_concept=custom_concept, seller_id=current_user.id)

        product.save()

        flash("Image uploaded")

        return redirect(url_for('sellers.new'))

    else:
        return redirect(url_for('sellers.new'))


@images_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@images_blueprint.route('/', methods=["GET"])
def index():
    pass


@images_blueprint.route('/<image_id>/edit', methods=['GET'])
def edit(image_id):
    # query = Image.delete().where(id == int(image_id))
    image = Image.get_by_id(int(image_id))
    query = image.delete_instance()
    username = current_user.username
    return redirect(url_for('users.show', username=username))


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
