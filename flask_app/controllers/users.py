from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workouts
# from flask_app.models.workout import Workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/registration')
def registration():
    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    password = request.form['password']
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form["email"],
        "password": pw_hash
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/log_in', methods=['post'])
def login_():
    user = User.get_from_email(request.form)


    
    print(user.password)
    if not user:

        flash("INVALID EMAIL address", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash( user.password, request.form['password']):
        print(user.password)
        flash("INVALID PASSWORD!!", "login")
        return redirect('/login')
    print(user.password)
    session['user_id'] = user.id
    return redirect('/dashboard')




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_from_id(data))


@app.route('/profile')
def profile():
    pass


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
