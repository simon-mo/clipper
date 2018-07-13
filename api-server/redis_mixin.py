import redis
import json
from contextlib import contextmanager
from config import REDIS_DB
from typing import Union


@contextmanager
def using_db(db_num: int):
    print(f"Using db {db_num}")
    yield redis.StrictRedis(db=db_num, decode_responses=True)


class RedisBaseMixin:
    @property
    def redis_key(self) -> str:
        key_name = self.Meta.primary_key

        if callable(key_name):
            key_name = key_name(self._dict)
        else:
            key_name = self._dict[key_name]

        return key_name

    @property
    def data_field(self) -> str:
        field_name = self.Meta.data_field
        data = self._dict[field_name]
        return data


    def save(self) -> Exception:
        raise NotImplementedError("To be implemented in child class")


class RedisSetMixin(RedisBaseMixin):
    """One to Many Mapping Redis Class

    Requires Meta Field:
        - db: The redis database number
        - redis_key
        - data_field
    """

    def save(self):
        with using_db(self.Meta.db) as client:
            client.sadd(self.redis_key, *self.data_field)

    @classmethod
    def get_all(cls, key):
        with using_db(cls.Meta.db) as client:
            result = client.smembers(key)

        if len(result) == 0:
            return None
        else:
            return cls(result, allow_coerce=True)


class RedisHashMixin(RedisBaseMixin):
    def save(self):
        with using_db(self.Meta.db) as client:
            client.hmset(self.redis_key, self._dict)

    def delete(self):
        with using_db(self.Meta.db) as client:
            client.delete(self.redis_key)

    def set(self, key, val):
        with using_db(self.Meta.db) as client:
            client.hset(self.redis_key, key, val)

    @classmethod
    def get_all(cls, key):
        with using_db(cls.Meta.db) as client:
            result = client.hgetall(key)
        if len(result) == 0:
            return None
        else:
            result = {k: _handle_array(v) for k,v in result.items()}
            return cls(result, allow_coerce=True)

def _handle_array(s:str) -> str:
    if s.startswith('[') and s.endswith(']'):
        s = s.replace("'", '"')
        return json.loads(s)
    else:
        return s

class RedisStringMixin(RedisBaseMixin):
    def save(self):
        with using_db(self.Meta.db) as client:
            client.set(self.redis_key, self.data_field)

    @classmethod
    def get(cls, key):
        with using_db(cls.Meta.db) as client:
            result = client.get(key)
        if result is None:
            return None
        else:
            return cls(result, allow_coerce=True)