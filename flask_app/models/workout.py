from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Workout:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.date = data['date']
        self.length = data['length']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def saveworkout(cls, data):
        query = 'INSERT INTO workout (type, date, length, description, user_id) VALUES (%(type)s,%(date)s,%(length)s,%(description)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_workouts(cls):
        query = "SELECT * FROM user JOIN workout ON user.id = workout.user_id"
        results = connectToMySQL(cls.db).query_db(query)

        workouts = []
        for row in results:
            data = {
                'id': row['workout.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'type': row['type'],
                'date': row['date'],
                'description': row['description'],
                'updated_at': row['workout.updated_at'],
                'created_at': row['workout.created_at'],
                'length': row['length'],
                'user_id': row['user_id']
            }
            workouts.append(cls(data))
        return workouts

    @classmethod
    def get_all_workouts_from_user(cls, data):
        query = "SELECT workout.* FROM user  JOIN workout ON user.id = workout.user_id WHERE user_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
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
        query = 'update workout set type=%(type)s, date=%(date)s, length=%(length)s, description=%(description)s where id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_workout_description(cls, data):
        query = 'select * from workout where description = %(description)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def delete_workout(cls, data):
        query = 'delete from workout where id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def user_workouts(cls, data):
        query = 'select * from workout join friends on workouts.id = friends.workout_id join users on friends.user_id = users.id'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        query = ' SELECT * FROM workout WHERE type = %(type)s;'
        results = connectToMySQL(Workout.db).query_db(query, workout)
        # if len(results) >= 1:  # to check if workout has been taken
        #     flash("Sorry, workout is already in there", "register")
        #     is_valid = False
        if len(workout['type']) < 2:
            flash("Workout needs a name", "register")
        if int(workout['length']) < 2:
            flash("comeon how long was it", "register")
        if len(workout['description']) < 6:
            flash("talk to me about this workout tell me more", "register")
        return is_valid
