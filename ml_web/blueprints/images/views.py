from flask import Blueprint, render_template
from ml_web.util.helper_clarifai import app_clarifai, predict_model_chair
from models.image import Image

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
@images_blueprint.route('/predict_chair', methods=['GET'])
def predict_chair():
    input_file=False #True if using local path. False if using URL
    model='Next_Academy_Project'
    image_path='https://ii.worldmarket.com/fcgi-bin/iipsrv.fcgi?FIF=/images/worldmarket/source/42812_XXX_v1.tif&wid=650&cvt=jpeg'
    result = predict_model_chair(image_path=image_path, model=model, input_file=input_file)

    # for x,y in result:
    #     print(f'The {x} concept has a {y} probability of matching your input.')

    print(result)

    return  "pass"
    
    # if result != "":
    #     for product_name, probability in result:
    #         product_name = product_name
    #     # breakpoint()
    #     image = Image.get_or_none(product_name == product_name)
    #     id = image.id
    #     return redirect(url_for('sellers.product', id=id))

    # else: 
    #     return render_template('images/new.html')