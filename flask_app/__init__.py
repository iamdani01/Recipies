from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "keep it secret"

bcrypt = Bcrypt(app)

DATABASE = "recipies_db"