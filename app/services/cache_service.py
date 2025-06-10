import json
from typing import Any, Optional, TypeVar, Generic, Type
from pydantic import BaseModel
import redis.asyncio as redis

from app.core.redis import get_redis

T = TypeVar('T', bound=BaseModel)

class CacheService(Generic[T]):
    def __init__(self, prefix: str, model_class: Type[T]):
        """
        Cache service for Redis
        
        Args:
            prefix: The prefix for cache keys
            model_class: The Pydantic model class for serialization/deserialization
        """
        self.prefix = prefix
        self.model_class = model_class
        
    def _get_key(self, key: str) -> str:
        """
        Get the full cache key with prefix
        """
        return f"{self.prefix}:{key}"
        
    async def get(self, key: str) -> Optional[T]:
        """
        Get an item from cache
        """
        redis_client = await get_redis()
        data = await redis_client.get(self._get_key(key))
        if data:
            return self.model_class.parse_raw(data)
        return None
        
    async def set(self, key: str, value: T, expire: int = 3600) -> bool:
        """
        Set an item in cache
        """
        redis_client = await get_redis()
        data = value.json()
        return await redis_client.setex(self._get_key(key), expire, data)
        
    async def delete(self, key: str) -> bool:
        """
        Delete an item from cache
        """
        redis_client = await get_redis()
        return await redis_client.delete(self._get_key(key)) > 0
        
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache
        """
        redis_client = await get_redis()
        return await redis_client.exists(self._get_key(key)) > 0
        
    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment a counter
        """
        redis_client = await get_redis()
        return await redis_client.incrby(self._get_key(key), amount)
