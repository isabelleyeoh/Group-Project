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
    pass


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


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


        