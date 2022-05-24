from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.workout import Workout
from flask_app.models.friend import Friend
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.image_path = data['image_path']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_img(cls, data):
        query = 'UPDATE user SET image_path = %(image_path)s WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def create_img(cls, data):
        query = 'UPDATE user SET image_path = %(image_path)s WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM user left join workout on user.id = workout.user_id order by workout.date DESC'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            user = cls(row)
            user.friends = cls.get_one_user_friend({"id": row['user_id']})
            user.workout = Workout.get_workout_id({"id": row['workout.id']})
            users.append(user)
        if len(results) < 1:
            return False
        return users

    @classmethod
    def get_all_user_friends(cls):
        query = 'select * from user join friendship on user.id = friendship.user_id'
        results = connectToMySQL(cls.db).query_db(query)
        usefriends = []
        for row in results:
            user = cls(row)
            user.friends = cls.get_one_user_friend({"id": row["user.id"]})
            usefriends.append(user)
        return usefriends

    @classmethod
    def get_one_user_friend(cls, data):
        query = ' select user.*, friendship.id from user join friendship on user.id = friendship.friend_id where user_id = %(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        friends = []
        for row in results:
            one_friend = cls(row)
            one_friend.friendship_id = row['friendship.id']
            friends.append(one_friend)
        return friends

    @classmethod
    def get_one_request_friend(cls, data):
        query = ' select u2.*, friendship.id from user join friendship on user.id = friendship.friend_id join user u2 on friendship.user_id = u2.id where friendship.friend_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        friends = []
        for row in results:
            one_friend = cls(row)
            one_friend.friendship_id = row['friendship.id']
            friends.append(one_friend)
        return friends

    @classmethod
    def get_from_id(cls, data):
        query = 'SELECT * FROM user where id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        user.friends = cls.get_one_user_friend({'id': results[0]['id']})
        user.friends_requests = cls.get_one_request_friend(
            {'id': results[0]['id']})
        if len(results) < 1:
            return False
        return user

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

    @classmethod
    def userfriendworkouts(cls, data):
        query = 'SELECT * FROM user JOIN friendship ON user.id=friendship.user_id LEFT JOIN user as user2 ON user2.id = friendship.friend_id left join workout on friendship.friend_id = workout.user_id where user.id = %(id)s'
        result = connectToMySQL(cls.db).query_db(query, data)
        user = cls(result[0])
        user.friends = []
        for f in result:
            friend = cls.get_from_id({'id': f['friendship.friend_id']})

            workoutdata = {
                'id': f['id'],
                'type': f['type'],
                'description': f['description'],
                'length': f['length'],
                'date': f['date'],
                'updatedat': f['updatedat'],
                'createdat': f['createdat'],
                'user_id': f['user_id']
            }

            friend.workout = Workout(workoutdata)
            user.friends.append(friend)
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = 'SELECT * FROM user WHERE email = %(email)s;'
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
