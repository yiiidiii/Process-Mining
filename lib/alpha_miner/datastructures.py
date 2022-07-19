import string
from typing import List, Union
import xes_parser.parser as xp
import alpha_miner.miner as am


class MyTransition:
    def __init__(self, name: string):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return str(other) == str(self)

    def __hash__(self):
        return hash(self.name)


def sort(a_list):
    return sorted(a_list, key=lambda l: l.name)


def string_list(t_list: List[MyTransition]):
    """
    method to create a string representation for a list of transitions
    :param t_list: list of MyTransition objects
    :return: string representation
    """
    result_str = ''
    for t in t_list:
        result_str = result_str + f'{t.name}, '
    return '{' + result_str.strip(', ') + '}'


class Place:
    _place_id = 1

    def __init__(self, in_list, out_list):
        self._place_id = Place._place_id
        Place._place_id += 1

        # for alpha miner, because miner.py only works with event-names for identification
        if (len(in_list) != 0 and all(isinstance(el, str) for el in in_list)) or \
                (len(out_list) != 0 and all(isinstance(el, str) for el in out_list)):
            self.in_list = list(sorted(in_list))
            self.out_list = list(sorted(out_list))
            for i in range(len(in_list)):
                self.in_list[i] = MyTransition(self.in_list[i])
            for o in range(len(out_list)):
                self.out_list[o] = MyTransition(self.out_list[o])
            self.name = str(self)

        # for unit tests
        else:
            self.in_list = sort(in_list)
            self.out_list = sort(out_list)
            if len(self.in_list) == 0:
                self.name = 'start'
            elif len(self.out_list) == 0:
                self.name = 'end'
            else:
                self.name = str(self)

    def __str__(self):
        if len(self.in_list) == 0:
            return 'start'
        elif len(self.out_list) == 0:
            return 'end'
        else:
            return 'p(' + string_list(self.in_list) + ', ' + string_list(self.out_list) + ')'

    def __eq__(self, other):
        if len(self.in_list) != len(other.in_list):
            return False
        if len(self.out_list) != len(other.out_list):
            return False
        for e in self.in_list:
            if e not in other.in_list:
                return False
        for e in self.out_list:
            if e not in other.out_list:
                return False
        return True


class Edge:
    def __init__(self, source: Union[MyTransition, Place], direction: Union[MyTransition, Place]):
        """
        one Edge in the petri net
        :param source: either transition or place
        :param direction: either transition or place
        """
        self.source = source
        self.direction = direction
        self.name = str(self)

    def __str__(self):
        return '(' + self.source.name + ', ' + self.direction.name + ')'

    def __eq__(self, other):
        if type(self.source) == type(other.source) and type(self.direction) == type(other.direction) and \
                self.source == other.source and self.direction == other.direction:
            return True
        return False


def main():
    # Transitions:
    """trans_a = MyTransition('a')
    trans_b = MyTransition('b')
    trans_c = MyTransition('c')
    trans_d = MyTransition('d')
    trans_e = MyTransition('e')
    correct_trans_list = [trans_a, trans_b, trans_c, trans_d, trans_e]
    # places:
    place_start = Place([], [trans_a])
    place_a_eb = Place([trans_a], [trans_e, trans_b])
    place_a_ec = Place([trans_a], [trans_e, trans_c])
    place_eb_d = Place([trans_e, trans_b], [trans_d])
    place_ec_d = Place([trans_e], [trans_c, trans_d])
    place_end = Place([trans_d], [])
    correct_place_list = [place_start, place_a_eb, place_a_ec, place_eb_d, place_ec_d, place_end]
    # correct edges
    correct_result = [Edge(trans_a, place_a_eb), Edge(place_a_eb, trans_e), Edge(place_a_eb, trans_b),
                      Edge(place_a_ec, trans_e), Edge(place_a_ec, place_ec_d), Edge(trans_e, place_eb_d),
                      Edge(trans_b, place_eb_d), Edge(place_eb_d, trans_d), Edge(trans_e, place_ec_d),
                      Edge(trans_c, place_ec_d), Edge(place_ec_d, trans_d), Edge(place_start, trans_a),
                      Edge(trans_d, place_end)]

    (header, body) = xp.prepare('log_data/L1.xes')
    traces = xp.parse_body(body)
    test_edges = am.step_7_create_edges(traces)
    test_places = am.step_6_create_places(traces)
    test_transitions = am.step_1_get_event_names_as_set(traces)

    return correct_place_list == test_places"""


if __name__ == '__main__':
    main()
    # trans_a = MyTransition('a')
    # trans_b = MyTransition('b')
    # trans_e = MyTransition('e')
    # transitions = string_list([trans_a, trans_b, trans_e])
    # place_a_eb = Place([trans_a], [trans_e, trans_b])
    # print(sort(place_a_eb.out_list))
