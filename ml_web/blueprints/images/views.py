from flask import Blueprint, render_template
from ml_web.helpers.helper_clarifai import app_clarifai, model_prediction
from models.image import Image
from models.product import Product


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


# Custom Model - predict chair type with input of local file
@images_blueprint.route('/prediction_result', methods=['GET'])
def prediction_result():

    input_file=True #True if using local path. False if using URL
    model='Next_Academy_Project'
    workflow_id="Furniture-1"
    # image_path = request.form['image_url']
    image_path='/Users/jianming/Desktop/Next_Academy_Python/Test_Photos/Group_Project/Concept_Ikea_Marius_Stool/Marius_Test_4.jpg'
    result = model_prediction(image_path=image_path, model=model, input_file=input_file, workflow_id=workflow_id)

    breakpoint()
    # Query the predicted concept and return the concept name
    query = Product.get_or_none(Product.concept==result[1][0][0])

    # Return search result
    if query:
        print(f'The object you have selected is the {query.name}. It has a price tag of RM{query.price}')
        
    else:
        print('Sorry - your image does not return any results.')

    return  "pass"
    