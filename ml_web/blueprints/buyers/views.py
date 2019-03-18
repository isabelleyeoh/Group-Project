from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.base_model import db, BaseModel
from models.user import User
from models.product import Product

from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# JM added
from ml_web.helpers.helper_aws import upload_file_to_s3, allowed_file
from werkzeug import secure_filename
from app import app

from PIL import Image as PILImage
from io import BytesIO  

from ml_web.helpers.helper_clarifai import app_clarifai, model_prediction

buyers_blueprint = Blueprint('buyers',
                            __name__,
                            template_folder='templates')


@buyers_blueprint.route('/new', methods=['GET'])
def new():
    return render_template("buyers/search_result.html")


@buyers_blueprint.route('/search', methods=["POST"])
def search():
    category = request.form['product']
    products = Product.select().where(Product.category == category)
    if products.exists():
        return render_template('sellers/product.html', products=products, category=category)
    else:
        return render_template('sellers/noproduct.html', category=category)
    
@buyers_blueprint.route('/search_result', methods=["POST"])
def index():
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
       
        # Define: Custom Model and Search Model tuple list

        cust_result_list=result[0]
        search_result_list=result[1]
        
        # Check: Exact Product Match
        if cust_result_list[0][1]>0.70:
            # Get matching model + recommended items
            search_result_list=search_result_list[:5]

            matching_products = Product.get_or_none(Product.concept==cust_result_list[0][0])
            # Check: Top 3 similar Products but omit matching model
            try:
                similar_products= Product.select().where(Product.clarifai_id << search_result_list,Product.clarifai_id!=matching_products.clarifai_id)
            except:
                similar_products=""
           
            match = True
            
        else:
            # Recomend items based on furniture type
            matching_products=""
            try:
                search_result_list=search_result_list[:4]
                # Check: Top 3 similar Products but omit matching model
                similar_products= Product.select().where(Product.clarifai_id << search_result_list)
            except:
                similar_products=""
            match = False

        # Render: template showing product result
        if len(similar_products)==0 and matching_products=="":
            return redirect(url_for('buyers.search_error'))
        else:
            return render_template("buyers/search_result.html", cust_result_list=cust_result_list,file_name=file.filename, match = match, matching_products=matching_products,similar_products=similar_products,search_image=image_url)

    return "Failed"



@buyers_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

# JM Search Error result
@buyers_blueprint.route('/search_error', methods=['GET'])
def search_error():

    return render_template("buyers/search_not_found.html")