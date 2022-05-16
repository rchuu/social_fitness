from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import workouts
from flask_app.controllers import friends

if __name__ == "__main__":
    app.run(debug=True)
