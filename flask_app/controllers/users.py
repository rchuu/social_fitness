from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/registration')
def registration():
    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form["email"],
        "password": password
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
    if not user:
        flash("EMAIL address not registered", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash( user.password, request.form['password']):
        flash("INVALID PASSWORD!!", "login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    workouts = Workout.get_all_workouts()
    return render_template('dashboard.html', user=User.get_from_id(data), workouts = workouts)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user_workouts = Workout.get_all_workouts_from_user(data)
    return render_template('view_profile.html', user_workouts = user_workouts)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
