from flask_app import app, bcrypt
from flask import render_template, session, request, redirect

# must import model but make sure to change the name
from flask_app.models.model_recipies import Recipe
from flask_app.models.model_user import User
from flask import flash

@app.route('/view/recipe/<int:id>')
def show_recipe(id):
    if 'uuid' not in session:
        return redirect('/')
    
    recipe = Recipe.get_one({'id':id})
    


    return render_template("view_one.html",recipe=recipe)

@app.route('/add')
def add_one():
    
    user = session['uuid']
    return render_template("add_recipe.html",user=user)


@app.route('/add/recipe',methods=["POST"])
def add_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect('/add')

    Recipe.add_recipe(request.form)
    return redirect("/dashboard")

@app.route('/edit/<int:id>')
def edit(id):
    recipe = Recipe.get_one({'id':id})
    return render_template("edit.html",recipe = recipe)

@app.route('/edit/recipe/', methods=['POST'])
def edit_recipe():
    if not Recipe.validate_recipe(request.form):
        id = request.form['id']
        return redirect(f'/edit/{id}')
    Recipe.edit_one(request.form)
    return redirect("/dashboard")

@app.route('/delete/<int:id>', methods = ['GET'])
def delete_one(id):
    Recipe.delete({'id':id})
    return redirect("/dashboard")