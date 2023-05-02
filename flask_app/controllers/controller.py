
from flask_app import app, bcrypt
from flask import render_template, session, request, redirect

# must import model but make sure to change the name
from flask_app.models.model_user import User
from flask_app.models.model_recipies import Recipe
from flask import flash
# Display route
@app.route('/')
def index():
    return render_template("index.html")

# Action route
@app.route('/create', methods=["POST"])
def user_create():
    if not User.validator(request.form):
        return redirect("/")

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'pw': hash_pw
    }

    id = User.user_add(data)
    session['uuid'] = id
    print(session['uuid'])
    return redirect("/")

# Display route
@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    
    all_recipies = Recipe.get_all()
    


    return render_template("log_in_page.html",all_recipies=all_recipies)

# Display route
@app.route('/user/login', methods=["POST"])
def user_process_login():
    if not User.validator_login(request.form):
        return redirect('/')
    print(session['uuid'])

    return redirect('/dashboard', )




# Action route
@app.route('/user/<int:id>/update', methods=["POST"])
def user_update(id):
    # do something
    return redirect("/")

# Action route
@app.route('/user/<int:id>/delete', methods=["POST"])
def user_delete(id):
    # do something
    return redirect("/")


