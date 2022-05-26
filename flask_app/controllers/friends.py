from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_app.models.friend import Friend


# I know this doesn't work yet but I wanted it here so we have a concept of what we need to work on
@app.route('/friend_profile/<int:id>')
def view_friend_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_workouts = Workout.get_all_workouts_from_user(data)
    user = User.get_from_id(data)
    friend = Friend.get_one_user_friends(data)
    num = Friend.num_friends(data)
    return render_template('view_profile.html', user_workouts=user_workouts, user=user, friend=friend, num=num)


@app.route('/addfriend/<int:id>')
def addfriend(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'friend_id': id,
        'requested_by': session['user_id']
    }
    Friend.add_friend(data)
    print(data)
    return redirect('/dashboard')


@app.route('/addfriend/accept/<int:id>')
def accept_friend(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': id,
        'friend_id': session['user_id']
    }
    print(data)

    Friend.approved_friend(data)
    new_data = {
        'user_id': session['user_id'],
        'friend_id': id,
        'requested_by': id
    }
    print(data)
    Friend.add_approved_friend(new_data)
    return redirect('/profile')


@app.route('/addfriend/decline/<int:id>')
def decline_friend(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': id,
        'friend_id': session['user_id']
    }
    print(data)
    Friend.decline_friend(data)
    return redirect('/profile')
