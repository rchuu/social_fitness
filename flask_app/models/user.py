from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.workout import workout
from flask_app.models.friend import friend
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = '''INSERT INTO user (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM user'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_from_id(cls, data):
        query = 'SELECT * FROM user where id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_from_email(cls, data):
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    # @classmethod
    # def users_and_workouts(cls,data):
    #     query = 'select * from workout join friends on workouts.id = friends.workout_id join users on friends.user_id = users.id'
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     if len(results) < 1:
    #         return False
    #     return cls(cls(results[0]))

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = ' SELECT * FROM user WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:  # to check if email has been taken
            flash("Sorry, email has been taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email format", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name needs at least 2 characters", "register")
        if len(user['last_name']) < 2:
            flash("Last name needs at least 2 characters", "register")
        if len(user['password']) < 6:
            flash("Password needs at least 6 characters", "register")
        if user['password'] != user['confirm']:
            flash("Does not match!", "register")
        return is_valid
