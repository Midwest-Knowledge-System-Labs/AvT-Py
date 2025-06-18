from typing import List
import avesterra as av
from dotenv import load_dotenv, find_dotenv
from orchestra.interface import ValueType
from event_handler.routable_event_handler import RoutableEventHandler
from avesterra import AvValue

load_dotenv(find_dotenv())

message_log: List[AvValue] = []

event_handler = RoutableEventHandler(
    name="MessageLogger",
    version="1.0.0",
    description="A cool published message logger",
    handling_threads=4,
    socket_count=8,
)
av.av_log.info(f"Starting with {event_handler._version=}")

@event_handler.route("A route that captures messages that have been published on entities that the event_handler outlet is subscribed to")
@event_handler.event(av.AvEvent.MESSAGE)
@event_handler.value_in(value_type=ValueType.text())
def echo(value: AvValue) -> av.AvValue:
    """This route captures MESSAGE events have been routed to the outlet via its subscriptions to entities"""
    message_log.append(value)

event_handler.run()