from flask import Blueprint, render_template
from ml_web.util.helper_clarifai import app_clarifai, predict_image_celebrity,predict_model_chair



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


@images_blueprint.route('/predict_celebrity', methods=['GET'])
def predict_celebrity():

    model='Celebrity'
    image=''
    result = predict_image_celebrity(image=image, model=model)

    print(result)

    return render_template('images/new.html')

# Custom Model - predict chair type with input of local file
@images_blueprint.route('/predict_chair', methods=['GET'])
def predict_chair():
    input_file=True #True if using local path. False if using URL
    model='Next_Academy_Project'
    image_path='/Users/jianming/Desktop/Herman_Miller_Test.jpeg'
    result = predict_model_chair(image_path=image_path, model=model, input_file=input_file)

    for x,y in result:
        print(f'The {x} concept has a {y} probability of matching your input.')

    return render_template('images/new.html')