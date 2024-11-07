# This file is used to manage the connection to the Redis database. It is a singleton class that creates a connection pool
import redis
from redis import ConnectionPool
from config import Config


class RedisConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls,db):
        if cls._pool is None:
            cls._pool = ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=db)
        return cls._pool


    @classmethod
    def get_connection(cls,db=0):
        return redis.Redis(connection_pool=cls.get_pool(db))
    

   
       



