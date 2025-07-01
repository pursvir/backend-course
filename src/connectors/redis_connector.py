import redis.asyncio as redis

class RedisManager:
    def __init__(self, url: str):
        self.url = url
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(self.url)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        return await self.redis.get(key) # type: ignore

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire) # type: ignore
        else:
            await self.redis.set(key, value) # type: ignore

    async def delete(self, key: str):
        await self.redis.delete(key) # type: ignore
