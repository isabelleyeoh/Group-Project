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

# *********JM TESTING UPLOAD OF IMAGE TO RUN THROUGH CLARIFAI **************#

@images_blueprint.route('/uploader', methods=['GET'])
def image_uploader():

    return render_template('images/uploader.html')

@images_blueprint.route('/search_result', methods=['POST'])
def search_result():
    # A: Check if there is file in form
    
    if "search_image" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["search_image"]
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
        image_url=output
        
        # Run image through Clarifai

        input_file=False #True if using local path. False if using URL
        model='Next_Academy_Project'
        workflow_id="Furniture-1"
        image_path=image_url #Get image url from AWS S3
        result = model_prediction(image_path=image_path, model=model, input_file=input_file, workflow_id=workflow_id)
       
        # Define: Custom Model and General Model tuple list

        cust_result_list=result[0]
        gen_result_list=result[1]

        # Check: Whether exact match or none

        # breakpoint()
        if cust_result_list[0][1]>0.70:
            # Get matching model + recommended items
            product_match = Product.get_or_none(Product.concept==cust_result_list[0][0])
            category_match=Product.select().where(Product.category==product_match.category, Product.concept!=cust_result_list[0][0])
            match = True
            
        else:
            # Recomend items based on furniture type
            product_match=""
            category_match=Product.select().where(Product.category==gen_result_list[0][0])
            match = False
        
        # Render: template showing product result
        return render_template("images/search_result.html", cust_result_list=cust_result_list, gen_result_list=gen_result_list,file_name=file.filename, match = match, product_match=product_match, category_match=category_match,search_image=image_url)


        