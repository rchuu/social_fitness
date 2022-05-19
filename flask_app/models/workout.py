from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Workouts:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.date = data['date']
        self.length = data['length']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @classmethod
    def saveworkout(cls, data):
        query = 'INSERT INTO workout (type, date, length, description) VALUES (%(type)s,%(date)s,%(length)s,%(description)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_workouts(cls):
        query = 'SELECT * FROM workout'
        results = connectToMySQL(cls.db).query_db(query)
        workouts = []
        for row in results:
            workouts.append(cls(row))
        return workouts

    @classmethod
    def get_workout_id(cls, data):
        query = 'SELECT * FROM workout where id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update_workout(cls, data):
        query = 'update workout set type=%(type)s, date=%(date)s, length=%(length)s, description=%(description)s, where id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_workout_description(cls, data):
        query = 'select * from workout where description = %(description)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    def delete_workout(cls, data):
        query = 'delete from workout where id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
# <<<<<<< updates
#     def friend_workouts(cls, data):
#         query = 'select * from user left join friendship on user.id = friendship.user_id left join workout on workout.user_id = friendship.friend_id where user.id = %(user)s'
# =======
#     def user_workouts(cls, data):
#         query = 'select * from workout join friends on workouts.id = friends.workout_id join users on friends.user_id = users.id'
# >>>>>>> main
#         results = connectToMySQL(cls.db).query_db(query, data)
#         if len(results) < 1:
#             return False
#         return cls(results[0])

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        query = ' SELECT * FROM workout WHERE name = %(name)s;'
        results = connectToMySQL(Workouts.db).query_db(query, workout)
        if len(results) >= 1:  # to check if workout has been taken
            flash("Sorry, workout is already in there", "register")
            is_valid = False
        if len(workout['name']) < 2:
            flash("Workout needs a name", "register")
        if int(workout['length']) < 2:
            flash("comeon how long was it", "register")
        if len(workout['description']) < 6:
            flash("talk to me about this workout tell me more", "register")
        return is_valid
