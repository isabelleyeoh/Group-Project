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


@images_blueprint.route('/new', methods=['GET'])
def new():

    pass


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
    return "images"


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


# Custom Model - predict chair type with input of local file
# @images_blueprint.route('/predict_chair', methods=['GET'])
# def predict_chair():
#     input_file=False #True if using local path. False if using URL
#     model='Next_Academy_Project'
#     image_path='https://www.ikea.com/my/en/images/products/stig-bar-stool-with-backrest-black__0438266_PE591356_S4.JPG'
#     result = predict_model_chair(image_path=image_path, model=model, input_file=input_file)

    # for x,y in result:
    #     print(f'The {x} concept has a {y} probability of matching your input.')

    # print(result)
    # return  "pass"
    
    # if result != "":
    #     for product_name, probability in result:
    #         product_name = product_name
    #     # breakpoint()
    #     image = Image.get_or_none(product_name == product_name)
    #     id = image.id
    #     return redirect(url_for('sellers.product', id=id))

    # else: 
    #     return render_template('images/new.html')