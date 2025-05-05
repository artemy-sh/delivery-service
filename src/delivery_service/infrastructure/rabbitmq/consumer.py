import json

import aio_pika

from delivery_service.application.dto.parcel import (
    ParcelDTO,
    map_dto_to_entity,
)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.use_cases.register_parcel import (
    RegisterParcelUseCase,
)
from delivery_service.infrastructure.config import settings


class ParcelConsumer:
    """
    Consumes parcel registration messages from RabbitMQ.
    """

    def __init__(
        self,
        register_parcel_uc: RegisterParcelUseCase,
        logger: ILogger,
        rabbitmq_url: str = settings.RABBITMQ_URL,
        queue_name: str = "register_parcel",
    ):
        self._rabbitmq_url: str = rabbitmq_url
        self._queue_name: str = queue_name
        self._register_parcel_uc: RegisterParcelUseCase = register_parcel_uc
        self._logger = logger

    async def start(self) -> None:
        """
        Listens to RabbitMQ queue and registers incoming parcels.
        """
        try:
            self._logger.info("[ParcelConsumer] Connecting to RabbitMQ...")
            connection = await aio_pika.connect_robust(self._rabbitmq_url)
            channel = await connection.channel()
            queue = await channel.declare_queue(self._queue_name, durable=True)
            self._logger.info(
                f"[ParcelConsumer] Waiting for messages on queue: {self._queue_name}"
            )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    self._logger.info(
                        "[ParcelConsumer] Received message:{message.body}"
                    )
                    async with message.process():
                        data = json.loads(message.body)
                        dto = ParcelDTO(**data)
                        parcel = map_dto_to_entity(dto)
                        await self._register_parcel_uc(parcel)
        except Exception as e:
            self._logger.error(
                f"Failed to publish message to RabbitMQ queue "
                f"{self._queue_name}: {e}"
            )
