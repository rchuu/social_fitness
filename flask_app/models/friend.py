from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, workout
from social_fitness.flask_app.models.workout import Workouts


class Friend:
    db = "social_fitness2"

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.date = data['date']
        self.length = data['length']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.workout = None


    @classmethod
    def friendworkouts(cls,data):
        query = 'select * from user left join friendship on user.id = friendship.user_id left join workout on workout.user_id = friendship.friend_id where user.id = %(id)s'
        result = connectToMySQL(cls.db).query_db(query,data)
        friends = []
        for f in result:
            friend = cls(f)
            
            workoutdata = {
                'id' : f['id'],
                'type' : f['type'],
                'description' : f['description'],
                'length' : f['length'],
                'date' : f['date'],
                'updatedat' : f['updatedat'],
                'createdat' : f['createdat'],
                'user_id' : f['user_id']
            }
            friend.workout = Workouts(workoutdata)
            friends.append(friend)
            print(t)
        return result