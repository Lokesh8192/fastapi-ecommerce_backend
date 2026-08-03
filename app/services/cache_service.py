import json

from app.core.redis import redis_client


class CacheService:

    @staticmethod
    def get(key: str):
        data = redis_client.get(key)

        if data:
            return json.loads(data)

        return None

    @staticmethod
    def set(
        key: str,
        value,
        expire: int = 300,
    ):
        redis_client.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    @staticmethod
    def delete(key: str):
        redis_client.delete(key)

    @staticmethod
    def clear():
        redis_client.flushdb()
