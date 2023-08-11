import threading
import pickle as pk
import redis


from ..config import Config  # noqa

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


class Redis(metaclass=Singleton):
    redis_instance = None

    def __init__(self):
        self.redis_instance = redis.StrictRedis(
                host=Config.config("REDIS_HOST"),
                port=Config.config("REDIS_PORT"),
                db=0,
                password=Config.config("REDIS_PASSWORD")
                if Config.config("REDIS_PASSWORD")
                else "",
            )
        print("Redis Initialized Successfully.")

    @staticmethod
    def cache(key, value, expire_in=None):
        val = pk.dumps(value)
        result = Redis().redis_instance.set(key, val)
        if expire_in:
            Redis().redis_instance.expire(key, expire_in)
        return result

    @staticmethod
    def acache(key, value, expire_in=None):
        cache_thread = threading.Thread(
            target=Redis().cache,
            args=(
                key,
                value,
            ),
            kwargs={"expire_in": expire_in},
        )
        cache_thread.start()

    @staticmethod
    def expire_in(key, seconds):
        Redis().redis_instance.expire(key, seconds)

    @staticmethod
    def get(key):
        if Redis().is_exist(key):
            val = Redis().redis_instance.get(key)
            value = pk.loads(val)
        else:
            value = None
        return value

    @staticmethod
    def is_exist(key):
        return True if Redis().redis_instance.exists(key) == 1 else False

    @staticmethod
    def delete(keys):
        for key in keys:
            Redis().redis_instance.delete(key)

    @staticmethod
    def deleteall():
        return Redis().redis_instance.flushall()

    @staticmethod
    def delete_current_db():
        return Redis().redis_instance.flushdb()

    @staticmethod
    def keys_count():
        return Redis().redis_instance.dbsize() - 1
