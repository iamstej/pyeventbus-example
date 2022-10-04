import asyncio
from collections import defaultdict
from typing import Dict

from subscriber import ISubscriber


class EventBus:
    """An event bus for adding/removing subscribers and publishing events to subscribers."""

    _subscribers: Dict[str, ISubscriber] = None

    def __init__(self):
        self._subscribers = defaultdict(list)

    def add_subscriber(self, key: str, subscriber: ISubscriber):
        """Add a subscriber to the event bus.

        :param key: The event key that the subscriber should respond to.
        :param subscriber: The subscriber object.
        """
        if subscriber in self._subscribers[key]:
            return

        self._subscribers[key].append(subscriber)

    def remove_subscriber(self, key: str, subscriber: ISubscriber):
        """Remove a subscriber from the event bus.

        :param key: The event key to remove the subscriber from.
        :param subscriber:
        :return:
        """
        if subscriber not in self._subscribers[key]:
            return

        self._subscribers[key].remove(subscriber)

    def publish_event(self, key: str, data: Dict):
        """Publish an event to all subscribers subscribed to the event key.

        :param key: The key to publish the event for.
        :param data: The data to pass to all subscribers.
        """
        for subscriber in self._subscribers[key]:
            asyncio.create_task(subscriber.handle(data))
