from typing import List


class Attribute:

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Event:
    _event_id = 0

    def __init__(self, attributes: List[Attribute]):
        self.event_id = Event._event_id
        Event._event_id += 1
        self.attributes = attributes


class Trace:
    def __init__(self, attributes: List[Attribute], events: List[Event]):
        self.attributes = attributes
        self.events = events

