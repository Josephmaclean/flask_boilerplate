from flask_sqlalchemy import SQLAlchemy as sq
import mongoengine as me
from app.utils import JSONEncoder
import json
import redis


class RedisService:
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, name, data):
        """

        :param name: {string} name of the object you want to set
        :param data: {Any} the object you want to set
        :return: {None}
        """
        if isinstance(data, sq().Model):
            json_data = json.dumps(data)
        elif isinstance(data, me.Document):
            json_data = JSONEncoder().encode(data.to_mongo())
        else:
            json_data = json.dumps(data)

        self.redis_conn.set(name, json_data)
        return True

    def get(self, name):
        """

        :param name:
        :return: {Any}
        """
        data = self.redis_conn.get(name)
        if data:
            return json.loads(data)
        return data