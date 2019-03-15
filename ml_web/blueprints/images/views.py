from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug import secure_filename
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from ml_web.helpers.helper_clarifai import app_clarifai, model_prediction
from models.image import Image
from models.product import Product

# JM added
from ml_web.helpers.helper_aws import upload_file_to_s3, allowed_file
from app import app

# JM added
from ml_web.helpers.helper_aws import upload_file_to_s3, allowed_file
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
 # A: Check if there is file in form
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]
    # print(file)

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):

        # Ensure correct orientation
        
        img = PILImage.open(file) #Create a Pillow file object

        if hasattr(img, '_getexif'):
            exifdata = img._getexif()
            try:
                orientation = exifdata.get(274)
                print(orientation)
                if orientation==6:  
                    img = img.rotate(-90)
                else:
                    pass
            except:
                pass
                # orientation = 1
        
        fs = BytesIO()
        # Save image with Pillow into FileStorage object.
        img.save(fs, format='JPEG')

        file.filename = secure_filename(file.filename)
        
        output = upload_file_to_s3(fs, file.filename, app.config["S3_BUCKET"], file.mimetype)
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        product_url=request.form['product_url']
        clarifai_id=request.form['clarifai_id']
        concept = request.form['concept']


        product = Product.create(image_url=str(output), name=name, description=description, category=category, price=price, concept=concept, seller_id=current_user.id, product_url=product_url, clarifai_id=clarifai_id)

        product.save()

        flash("Image uploaded")

        id=current_user.id
        return redirect(url_for('sellers.show', id=id))

    else:
        id=current_user.id
        return redirect(url_for('sellers.show', id=id))


@images_blueprint.route('/<image_id>/edit', methods=['GET'])
def edit(image_id):
    # query = Image.delete().where(id == int(image_id))
    image = Image.get_by_id(int(image_id))
    query = image.delete_instance()
    username = current_user.username
    return redirect(url_for('users.show', username=username))



