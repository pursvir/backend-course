import logging

import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, url: str):
        self.url = url

    async def connect(self):
        self._redis = await redis.from_url(self.url)
        logging.info(f"Connected to Redis instance under URL={self.url}")

    async def close(self):
        if self._redis:
            await self._redis.close()

    async def get(self, key: str):
        return await self._redis.get(key)

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def delete(self, key: str):
        await self._redis.delete(key)
