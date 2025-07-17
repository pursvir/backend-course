from src.config import settings
from src.connectors.redis_connector import RedisManager

redis_manager = RedisManager(url=settings.REDIS_URL)
