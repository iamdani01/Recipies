# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app import DATABASE, bcrypt
from flask import flash,session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# NOTE change table mname and database name
class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod 
    def get_all(cls):
        query = "select * from users"
        results =  connectToMySQL(DATABASE).query_db(query)
        all_users=[]
        for dict in results:
            all_users.append( cls(dict) )
        return all_users #returns a list of instances

    @classmethod
    def user_add(cls,data):
        query= "insert into users(first_name,last_name,email,pw) values(%(first_name)s,%(last_name)s,%(email)s,%(pw)s)"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results




    @classmethod 
    def log_in(cls):
        pass

    @classmethod
    def get_one(cls,data):
        query = "select* from users where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_one_by_email(cls,data):
        query = "select* from users where email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False
        return cls(result[0])


    @staticmethod
    def validator(data):
        is_valid = True

        if not data['first_name']:
            is_valid = False
            flash("first name is required", "err_user_first_name")

        if not data['last_name']:
            is_valid = False
            flash("last name is required", "err_user_last_name")

        if not data['email']:
            is_valid = False
            flash("email is required", "err_user_email")
        elif not EMAIL_REGEX.match(data['email']):
            flash("invalid email adress", "err_user_email")
            is_valid = False

        else:
            potential_user = User.get_one_by_email(data)
            if potential_user:
                is_valid= False
                flash("Email is already in use!", "err_user_email")

        if not data['pw']:
            is_valid = False
            flash("password is required", "err_user_pw")

        if not data['con_pw']:
            is_valid = False
            flash("confirm password is required", "err_user_con_pw")

        elif data['con_pw'] != data['pw']:
            is_valid = False
            flash("passwords do not match", "err_user_con_pw")

        return is_valid


    @staticmethod
    def validator_login(data):
        is_valid = True

        if not data['email']:
            is_valid = False
            flash("email is required", "err_user_login_email")
        elif not EMAIL_REGEX.match(data['email']):
            flash("invalid email adress", "err_user_login_email")
            is_valid = False

        if not data['pw']:
            is_valid = False
            flash("password is required", "err_user_login_pw")

        if is_valid:
            potential_user= User.get_one_by_email(data)
            if not potential_user:
                is_valid= False
                flash("invalid credentials", "err_user_login_pw")
            else:
                if not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                    is_valid = False
                    flash("invalid credentials", "err_user_login_pw")
                else:
                    session['uuid']= potential_user.id
        
        return is_valid


