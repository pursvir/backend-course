from src.connectors.redis_connector import RedisManager
from src.config import settings

redis_manager = RedisManager(url=settings.REDIS_URL)
