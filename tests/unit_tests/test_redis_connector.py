from src.init import redis_manager

async def test_redis_connection():
    await redis_manager.connect()
    # may raise redis.exceptions.ConnectionError
    await redis_manager._redis.ping()
