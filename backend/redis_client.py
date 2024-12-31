import redis

class RedisClient():
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = redis.Redis(host="localhost", port="6379", decode_responses=True)
        return cls._instance