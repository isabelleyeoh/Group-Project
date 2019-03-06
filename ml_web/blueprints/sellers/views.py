from flask import Blueprint, render_template


sellers_blueprint = Blueprint('sellers',
                            __name__,
                            template_folder='templates')


@sellers_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sellers/new.html')


@sellers_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['password']
    hashed_password = generate_password_hash(user_password)

    seller = Seller(username=request.form['username'],
                email=request.form['email'], password=hashed_password)

    if seller.save():
        flash("Successfully registered")
        session['username'] = request.form['username']
        login_user(seller)
        return redirect(url_for('sellers.index'))
    else:
        return render_template('sellers/new.html', username=request.form['username'], email=request.form['email'], password=request.form['password'], errors=seller.errors)


@sellers_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sellers_blueprint.route('/', methods=["GET"])
def index():
    return "sellers"


@sellers_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sellers_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
