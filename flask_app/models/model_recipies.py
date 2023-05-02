from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask import flash,session
from flask_app import DATABASE

class Recipe:
    def __init__( self, data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.under = data['under']
        self.user_id = data['user_id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']

    @classmethod
    def add_recipe(cls,data):
        query= "insert into recipies(name,under,user_id,description,instructions,date) values (%(name)s, %(under)s,%(user_id)s,%(description)s,%(instructions)s,%(date)s)"
        results = connectToMySQL(DATABASE).query_db(query,data)

        return results

    @classmethod 
    def get_all(cls):
        query = "select * from recipies join users on recipies.user_id=users.id;"
        results =  connectToMySQL(DATABASE).query_db(query)
        all_recipies=[]
        for dict in results:
            user_data={
                'id': dict['users.id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'pw' : dict['pw'],
                'created_at' : dict['users.created_at'],
                'updated_at' : dict['users.updated_at'],
            }
            user_instance = model_user.User(user_data)
            recipe=cls(dict)
            recipe.user=user_instance
            all_recipies.append(recipe)
        return all_recipies #returns a list of instances

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if not data['name']:
            is_valid = False
            flash("Name is required", "err_recipe_name")
        
        if not data["description"]:
            is_valid = False
            flash("description is required", "err_recipe_description")

        if not data['instructions']:
            is_valid = False
            flash("Instructions is required", "err_recipe_instructions")

        if not data['date']:
            is_valid = False
            flash("date is required", "err_recipe_date")

        if not data['under']:
            is_valid = False
            flash("please select one, err_recipe_under")
        return is_valid

    @classmethod
    def get_one(cls,data):
        query = "select* from recipies where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def edit_one(cls,data):
        query = "update recipies set name=%(name)s, description=%(description)s, instructions=%(instructions)s,date=%(date)s,under=%(under)s WHERE id = %(id)s;" 
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query= "delete from recipies where id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result