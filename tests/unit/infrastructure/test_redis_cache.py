from unittest.mock import AsyncMock

import pytest

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.infrastructure.services.redis_cache import RedisCache


@pytest.mark.anyio
async def test_redis_cache_get_and_set(
    fake_redis_client: AsyncMock, fake_logger: ILogger
) -> None:
    fake_redis_client.get.return_value = '"test_value"'

    cache = RedisCache(logger=fake_logger)
    cache._redis = fake_redis_client

    await cache.set("test_key", "test_value", ttl=100)

    result = await cache.get("test_key")
    assert result == "test_value"
