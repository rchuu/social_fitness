from sqlite3 import Row
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, workout, friend
from flask_app.models.workout import Workout


class Friend:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.friend_id=data['friend_id']



    @classmethod
    def add_friend(cls,data):
        query = 'insert into friendship (user_id, friend_id) values (%(user_id)s, %(friend_id)s)'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all_friends(cls):
        query = 'select * from friendship'
        results =  connectToMySQL(cls.db).query_db(query)
        friends = []
        for f in results:
            friends.append(cls(f))
        return friends

    @classmethod

    def get_one_user_friends(cls, data):
        query = 'SELECT * FROM user JOIN friendship ON user.id=friendship.user_id LEFT JOIN user as user2 ON user2.id = friendship.friend_id where friendship.user_id = %(id)s'
        # query = 'select freindship.* from user join friendship on user.id = friendship.user_id where user.id = %(id)s'
        results = connectToMySQL(cls.db).query_db(query,data)
        friends = []
        for row in results:
            friends.append(user.User(row))
        return friends
