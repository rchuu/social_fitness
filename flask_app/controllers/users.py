from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_app.models.friend import Friend
from flask_bcrypt import Bcrypt
from flask_app.models.friend import Friend
# --uploading image syntax start
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/richardchu/Documents/codingdojo/group_project/social_fitness/flask_app/static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/post/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                'id': session["user_id"],
                'image_path': "../static/img/" + filename,
            }
            User.create_img(data)
        return redirect('/profile')


# --uploading image syntax end
bcrypt = Bcrypt(app)


@ app.route('/registration')
def registration():
    return render_template("registration.html")


@ app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form["email"],
        "password": password,
    }
    id = User.save(data)
    if not id:
        flash("Email already taken, please login")
        return redirect('/')
    session['user_id'] = id
    return redirect('/dashboard')


@ app.route('/')
def index():
    return render_template("index.html")


@ app.route('/login')
def login():
    return render_template("login.html")


@ app.route('/log_in', methods=['POST'])
def login_():
    user = User.get_from_email(request.form)
    if not user:
        flash("EMAIL address not registered", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("INVALID PASSWORD!!", "login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')


@ app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    # everything = User.userfriendworkouts()
    # workouts = Workout.get_all_workouts()
    users = User.get_all()
    friends = Friend.get_all_friends()
    return render_template('dashboard.html', loggin_user=User.get_from_id(data), users=users, friends=friends)


@ app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user_workouts = Workout.get_all_workouts_from_user(data)
    user = User.get_from_id(data)
    friend = Friend.get_one_user_friends(data)
    pending_friends = Friend.get_pending_friends(data)
    approved_friends = Friend.get_approved_friends(data)
    request_friends = Friend.get_request_friends(data)
    num = Friend.num_friends(data)
    return render_template('view_profile.html', user_workouts=user_workouts, user=user, request_friends=request_friends, friend=friend, num=num, pending=pending_friends, approved=approved_friends)


@ app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
