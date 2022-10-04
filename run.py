import asyncio
from uuid import uuid4

import bus
import subscriber


async def main():
    # Initialise the event bus.
    event_bus = bus.EventBus()

    # Initialise the subscribers.
    printing_subscriber = subscriber.OrderPrintingSubscriber()
    email_subscriber = subscriber.OrderEmailSubscriber()
    notification_subscriber = subscriber.OrderNotificationSubscriber()

    # Register the subscribers to the event bus.
    event_bus.add_subscriber("order.created", printing_subscriber)
    event_bus.add_subscriber("order.created", email_subscriber)
    event_bus.add_subscriber("order.created", notification_subscriber)

    # Trigger an event.
    event_bus.publish_event("order.created", {"identifier": str(uuid4())})
    await asyncio.sleep(4)  # Await here so we can see the results of the subscribers which have a max 3s sleep in.


if __name__ == "__main__":
    asyncio.run(main())
