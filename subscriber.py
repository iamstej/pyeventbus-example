import abc
import asyncio
import time
from typing import Dict

# Interfaces


class ISubscriber(abc.ABC):
    """An interface that all subscribers should adhere to."""

    @abc.abstractmethod
    async def handle(self, data: Dict, *args, **kwargs):
        """A function for handling published events.

        :param data: The data passed from the published event.
        """
        ...


# Implementation


class OrderPrintingSubscriber(ISubscriber):
    """A subscriber for handling printing an order."""

    async def handle(self, data, *args, **kwargs):
        await asyncio.sleep(1)
        identifier = data.get("identifier")
        print(f"Sending order {identifier} to printer queue at {time.time()}...")


class OrderEmailSubscriber(ISubscriber):
    """A subscriber for handling emailing an order."""

    async def handle(self, data, *args, **kwargs):
        await asyncio.sleep(2)
        identifier = data.get("identifier")
        print(f"Sending order {identifier} to emailer queue at {time.time()}...")


class OrderNotificationSubscriber(ISubscriber):
    """A subscriber for handling sending push notifications regarding an order."""

    async def handle(self, data, *args, **kwargs):
        await asyncio.sleep(3)
        identifier = data.get("identifier")
        print(
            f"Sending order {identifier} to push notification service at {time.time()}..."
        )
