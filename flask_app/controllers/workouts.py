from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workouts



@app.route('/add_workout/', methods=['post'])
def addWorkout(cls, data):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workouts.validate_workout(request.form):
        return redirect('/new/sight')
    data={
        "type":request.form['type'],
        "date":request.form['date'],
        "length":request.form['length'],
        "description": request.form['description'],
        "id":id
    }
    Workouts.saveworkout(data)
    return redirect('/profile')

@app.route('/edit_workout/<int:id>')
def updateWorkout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    userdata = {
        "id":session['user_id']
    }
    return render_template('edit_workout.html', workout = Workouts.get_workout_id(data), user = User.get_from_id(userdata))

@app.route('/update_workout/<int:id>')
def update_workout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workouts.validate_workout(request.form):
        return redirect('/edit_workour/<int:id>')
    data={
        "type":request.form['type'],
        "date":request.form['date'],
        "length":request.form['length'],
        "description": request.form['description'],
        "id":id
    }
    Workouts.update_workout(data)
    return redirect('/profile')

@app.route('/view/workout/<int:id>')
def view_workout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    userdata = {
        "id":session['user_id']
    }
    return render_template('view_workout.html', workout = Workouts.get_workout_id(data), user = User.get_from_id(userdata))

@app.route('/delete_workout/<int:id>')
def delete_workout(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Workouts.delete_workout(data)
    return redirect('/profile')
