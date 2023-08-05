import sys
import threading
import pickle as pk
import redis

sys.path.append("..")
from config import Config  # noqa

lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(
                        *args, **kwargs
                    )
        return cls._instances[cls]


def with_redis_instance(func):
    def wrapper_func(*args, **kwargs):
        if not Redis._instance:
            Redis.get_instance()
        return func(*args, **kwargs)

    return wrapper_func


class Redis(metaclass=Singleton):
    _instance = None
    redis_instance = None

    @staticmethod
    def get_instance():
        if Redis.redis_instance is None:
            rd = redis.StrictRedis(
                host=Config.config("REDIS_HOST"),
                port=Config.config("REDIS_PORT"),
                db=0,
                password=Config.config("REDIS_PASSWORD")
                if Config.config("REDIS_PASSWORD")
                else "",
            )
            Redis(rd)
        return Redis._instance

    def __init__(self, redis_instance):
        Redis.redis_instance = redis_instance
        Redis._instance = self
        print("Redis Initialized Successfully.")

    @staticmethod
    @with_redis_instance
    def cache(key, value, expire_in=None):
        val = pk.dumps(value)
        result = Redis.redis_instance.set(key, val)
        if expire_in:
            Redis.redis_instance.expire(key, expire_in)
        return result

    @staticmethod
    @with_redis_instance
    def acache(key, value, expire_in=None):
        cache_thread = threading.Thread(
            target=Redis.cache,
            args=(
                key,
                value,
            ),
            kwargs={"expire_in": expire_in},
        )
        cache_thread.start()

    @staticmethod
    @with_redis_instance
    def expire_in(key, seconds):
        Redis.redis_instance.expire(key, seconds)

    @staticmethod
    @with_redis_instance
    def get(key):
        if Redis.is_exist(key):
            val = Redis.redis_instance.get(key)
            value = pk.loads(val)
        else:
            value = None
        return value

    @staticmethod
    @with_redis_instance
    def is_exist(key):
        return True if Redis.redis_instance.exists(key) == 1 else False

    @staticmethod
    @with_redis_instance
    def delete(keys):
        for key in keys:
            Redis.redis_instance.delete(key)

    @staticmethod
    @with_redis_instance
    def deleteall():
        return Redis.redis_instance.flushall()

    @staticmethod
    @with_redis_instance
    def delete_current_db():
        return Redis.redis_instance.flushdb()

    @staticmethod
    @with_redis_instance
    def keys_count():
        return Redis.redis_instance.dbsize() - 1
