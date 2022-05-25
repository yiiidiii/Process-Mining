from datetime import date
from tokenize import String
import string
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
    def __init__(self, trace_id: string, events: List[Event]):
        self.trace_id = trace_id
        self.events = events

