from multiprocessing import Event
import string
from typing import List


class Trace:
    def __init__(self, trace_id: string, events: List[Event]):
        self.trace_id = trace_id
        self.events = events