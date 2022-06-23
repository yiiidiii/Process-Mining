import string
from typing import List


class MyTransition:
    def __init__(self, name: string):
        self.name = name

    def __str__(self):
        return str(self.name)


class Place:
    _place_id = 1

    def __init__(self, in_list: List[MyTransition], out_list: List[MyTransition]):
        self._place_id = Place._place_id
        Place._place_id += 1
        self.in_list = in_list
        self.out_list = out_list
        self.name = str(self)

    def __str__(self):
        if len(self.in_list) == 0:
            return 'start'
        elif len(self.out_list) == 0:
            return 'end'
        else:
            return 'p(' + str(self.in_list) + ', ' + str(self.out_list) + ')'


class Edge:
    def __init__(self, source, direction):
        """
        one Edge in the petri net
        :param source: either transition or place
        :param direction: either transition or place
        """
        self.source = source
        self.direction = direction

    def __str__(self):
        return '(' + str(self.source) + ', ' + str(self.direction) + ')'
