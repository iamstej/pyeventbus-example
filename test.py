from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from uuid import uuid4

import bus
import subscriber


class EventBusTestCase(IsolatedAsyncioTestCase):
    """Test case for testing the event bus."""

    def setUp(self) -> None:
        """Set up the event bus with the subscribers available to the project."""
        # Initialise the event bus.
        self.event_bus = bus.EventBus()

        # Initialise the subscribers.
        self.printing_subscriber = subscriber.OrderPrintingSubscriber()
        self.email_subscriber = subscriber.OrderEmailSubscriber()
        self.notification_subscriber = subscriber.OrderNotificationSubscriber()

    async def test_event_bus_add_subscriber(self):
        """Test adding subscribers to the event bus works as expected."""
        # Register the subscribers to the event bus.
        self.event_bus.add_subscriber("order.created", self.printing_subscriber)
        self.event_bus.add_subscriber("order.created", self.email_subscriber)
        self.event_bus.add_subscriber("order.created", self.notification_subscriber)
        self.event_bus.add_subscriber("order.created", self.notification_subscriber)

        self.assertListEqual(
            self.event_bus._subscribers["order.created"],
            [
                self.printing_subscriber,
                self.email_subscriber,
                self.notification_subscriber,
            ],
        )

    async def test_event_bus_remove_subscriber(self):
        """Test removing subscribers from the event bus works as expected."""
        # Register the subscribers to the event bus.
        self.event_bus.add_subscriber("order.created", self.printing_subscriber)
        self.event_bus.add_subscriber("order.created", self.email_subscriber)
        self.event_bus.add_subscriber("order.created", self.notification_subscriber)
        self.event_bus.remove_subscriber("order.created", self.email_subscriber)

        self.assertListEqual(
            self.event_bus._subscribers["order.created"],
            [
                self.printing_subscriber,
                self.notification_subscriber,
            ],
        )

    async def test_event_bus_remove_unknown_subscriber(self):
        """Test removing subscribers from the event bus works as expected."""
        # Remove a subscriber which is not already registered.
        self.event_bus.remove_subscriber("order.created", self.email_subscriber)

        self.assertListEqual(self.event_bus._subscribers["order.created"], [])

    @patch.object(subscriber.OrderPrintingSubscriber, "handle")
    @patch.object(subscriber.OrderEmailSubscriber, "handle")
    @patch.object(subscriber.OrderNotificationSubscriber, "handle")
    async def test_event_bus_publish_event(self, *args, **kwargs):
        """Test that an event bus works as expected from initialisation through to publishing an event."""
        # Register the subscribers to the event bus.
        self.event_bus.add_subscriber("order.created", self.printing_subscriber)
        self.event_bus.add_subscriber("order.created", self.email_subscriber)
        self.event_bus.add_subscriber("order.created", self.notification_subscriber)

        # Trigger an event.
        self.event_bus.publish_event("order.created", {"identifier": str(uuid4())})

        # Assert all subscribers are called.
        self.printing_subscriber.handle.assert_called_once()
        self.email_subscriber.handle.assert_called_once()
        self.notification_subscriber.handle.assert_called_once()

    @patch.object(subscriber.OrderPrintingSubscriber, "handle")
    @patch.object(subscriber.OrderEmailSubscriber, "handle")
    @patch.object(subscriber.OrderNotificationSubscriber, "handle")
    async def test_event_bus_publish_unknown_event(self, *args, **kwargs):
        """Test that publishing an event with an unknown key doesn't cause any issues and doesn't trigger events."""
        # Register the subscribers to the event bus.
        self.event_bus.add_subscriber("order.created", self.printing_subscriber)
        self.event_bus.add_subscriber("order.created", self.email_subscriber)
        self.event_bus.add_subscriber("order.created", self.notification_subscriber)

        # Trigger an event.
        self.event_bus.publish_event("order.declined", {"identifier": str(uuid4())})

        # Assert all subscribers are called.
        self.printing_subscriber.handle.assert_not_called()
        self.email_subscriber.handle.assert_not_called()
        self.notification_subscriber.handle.assert_not_called()
