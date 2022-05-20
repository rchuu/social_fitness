from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_app.models.friend import Friend
from flask_app.controllers import users


@app.route('/add')
def add_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("add_workout.html", user=User.get_one(data))


@app.route('/add_workout', methods=['post'])
def addWorkout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect('/add')
    data = {
        "type": request.form['type'],
        "date": request.form['date'],
        "length": request.form['length'],
        "description": request.form['description'],
        'user_id': session['user_id']
    }
    Workout.saveworkout(data)
    return redirect('/profile')


@app.route('/edit_workout/<int:id>')
def updateWorkout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    userdata = {
        "id": session['user_id']
    }
    workout = Workout.get_workout_id(data)
    user = User.get_from_id(userdata)
    return render_template('edit_workout.html', workout=workout, user=user)


@app.route('/update_workout', methods = ['POST'])
def update_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect('/edit_workout/<int:id>')
    data = {
        "type": request.form['type'],
        "date": request.form['date'],
        "length": request.form['length'],
        "description": request.form['description'],
        "id": request.form['id'],
    }
    Workout.update_workout(data)
    return redirect('/profile')


@app.route('/view/workout/<int:id>')
def view_workout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    userdata = {
        "id": session['user_id']
    }
    workout = Workout.get_workout_id(data)
    user = User.get_from_id(userdata)
    return render_template('view_workout.html', workout=workout, user=user)


@app.route('/delete_workout/<int:id>')
def delete_workout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Workout.delete_workout(data)
    return redirect('/profile')
