from flask_app import app
# import all controller files
from flask_app.controllers import controller, controller_recipe

# must be at the bottom
if __name__ == "__main__":
    app.run(debug=True,port = 5001)
