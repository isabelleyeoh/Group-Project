from flask import Blueprint, render_template, request
from ml_web.helpers.helper_clarifai import app_clarifai, model_prediction
from models.image import Image
from models.product import Product

# JM added
from ml_web.helpers.helper_aws import upload_file_to_s3, allowed_file
from werkzeug import secure_filename
from app import app


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

# *********JM TESTING UPLOAD OF IMAGE TO RUN THROUGH CLARIFAI **************#

@images_blueprint.route('/test_upload', methods=['GET'])
def image_test():

    return render_template('images/test_upload.html')

@images_blueprint.route('/upload', methods=['POST'])
def image_upload():
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

        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])

        image_url=app.config['S3_LOCATION'] + file.filename

        breakpoint()

        input_file=False #True if using local path. False if using URL
        model='Next_Academy_Project'
        workflow_id="Furniture-1"
        image_path=image_url
        result = model_prediction(image_path=image_path, model=model, input_file=input_file, workflow_id=workflow_id)

        breakpoint()
        # Query the predicted concept and return the concept name
        query = Product.get_or_none(Product.concept==result[1][0][0])

        # Return search result
        if query:
            print(f'The object you have selected is the {query.name}. It has a price tag of RM{query.price}')
            
        else:
            print('Sorry - your image does not return any results.')
 
        # return redirect(url_for('users.edit',id=id))
        return "PASS IMAGE"

    else:
        return render_template("home.html")

