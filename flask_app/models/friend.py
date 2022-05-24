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
        self.requested_by = data['requested_by']



    @classmethod
    def add_friend(cls,data):
        query = 'insert into friendship (user_id, friend_id, requested_by) values (%(user_id)s, %(friend_id)s, %(requested_by)s)'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def add_approved_friend(cls,data):
        query = 'insert into friendship (user_id, friend_id, requested_by, status) values (%(user_id)s, %(friend_id)s, %(requested_by)s, "APPROVED");'
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
        query = 'SELECT user.first_name, user.last_name, user2.id as friend_id, user2.first_name as friend_first_name, user2.last_name as friend_last_name FROM user JOIN friendship ON user.id = friendship.user_id LEFT JOIN user as user2 ON user2.id = friendship.friend_id WHERE user_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def approved_friend(cls,data):
        query = 'update friendship set status = "APPROVED" WHERE user_id = %(user_id)s and friend_id = %(friend_id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def decline_friend(cls,data):
        query = 'delete from friendship WHERE user_id = %(user_id)s and friend_id = %(friend_id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_approved_friends(cls,data):
        query = "select u2.*, f.id from user u left join friendship f on u.id = f.user_id join user u2 on f.friend_id = u2.id where f.user_id = %(id)s and f.status = 'APPROVED';"
        results = connectToMySQL(cls.db).query_db(query, data)
        friends = []
        if not results:
            return friends
        for row in results:
            one_friend = user.User(row)
            one_friend.friendship_id = row['friendship.id']
            friends.append(one_friend)
        return friends

    @classmethod
    def get_request_friends(cls,data):
        query = "select u2.*, f.id from user u left join friendship f on u.id = f.user_id join user u2 on f.friend_id = u2.id where u.id = %(id)s and requested_by = %(id)s AND f.status = 'PENDING';"
        results = connectToMySQL(cls.db).query_db(query, data)
        friends = []
        if not results:
            return friends
        for row in results:
            one_friend = user.User(row)
            one_friend.friendship_id = row['f.id']
            friends.append(one_friend)
        return friends

    @classmethod
    def get_pending_friends(cls,data):
        query = "select u.*, f.id from user u left join friendship f on u.id = f.user_id join user u2 on f.friend_id = u2.id where f.friend_id= %(id)s and f.status = 'PENDING';"
        results = connectToMySQL(cls.db).query_db(query, data)
        friends = []
        if not results:
            return friends
        for row in results:
            one_friend = user.User(row)
            one_friend.friendship_id = row['f.id']
            friends.append(one_friend)
        return friends



    @classmethod
    def num_friends(cls,data):
        query = 'SELECT user.first_name, user.last_name, count(user.id) as num from friendship JOIN user on user.id = friendship.user_id WHERE user_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def friend_list_requests(self,data):
        query = 'insert into friendship (status, user_id, friend_id) values (%(status)s, %(user_id)s, %(friend_id)s),'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def delete_friend(cls, data):
        query = 'delete from friendship where id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

