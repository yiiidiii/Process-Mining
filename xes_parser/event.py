from datetime import date
import string
from tokenize import String


class Event:
    _event_id = 0

    def __init__(self, activity: String, timestamp: date, resource, transition: string):
        self.event_id = Event._event_id
        Event._event_id += 1
        self.timestamp = timestamp
        self.activity = activity
        self.resource = resource
        self.transition = transition