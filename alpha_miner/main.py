from xes_parser.datastructure import *
from xes_parser.main import *
import warnings
import alpha_miner.datastructures as ds


def get_event_names_as_set(traces: List[Trace]):
    """
    Fist step of alpha algorithm: extracts all the names of all events without duplicates (as set)
    :param traces: list of traces
    :return: set of event names
    """

    all_events = []
    for trace in traces:
        all_events = list(all_events + trace.events)

    event_names = event_list_to_name_list(all_events)

    return list(set(event_names))


def get_all_tuple_combinations(name_list):
    """
    computes every combination of two name elements in the name_list
    :param name_list: list of event names
    :return: list of tuples of every pairwise name combinations
    """

    tuple_list = []
    for i in range(0, len(name_list)):
        for j in range(0, len(name_list)):
            tuple_list.append((name_list[i], name_list[j]))

    return tuple_list


def first_last_event_names(traces: List[Trace]):
    """
    Second and third step of alpha algorithm: extracts the names of all first and last events in the list of traces
    :param traces: list of traces in the log file
    :return: set of names of the first events, list of names of last events
    """

    # take the events from the trace objects
    all_events = []
    for trace in traces:
        all_events.append(trace.events)

    # take the first element from each the event lists
    first_events = [event[0] for event in all_events]
    last_events = [event[-1] for event in all_events]

    # names of the fist events taken from their attribute list
    first_event_names = event_list_to_name_list(first_events)

    # names of the last events taken from their attribute list
    last_event_names = event_list_to_name_list(last_events)

    return set(first_event_names), set(last_event_names)


def map_all_events_to_name(traces: List[Trace]):
    """
    maps all the events in the lists of events to their respective names
    :param traces: list of traces
    :return: list of lists that contain the names of the events
    """

    all_events = []
    for trace in traces:
        all_events.append(trace.events)

    all_names = list(map(lambda e: event_list_to_name_list(e), all_events))

    return all_names


def event_list_to_name_list(events: List[Event]):
    """
    helper method for map_all_events_to_name: for each event in event list, extract their names
    :param events: list of events
    :return: list of names (string)
    """

    names = []
    for event in events:
        for attrib in event.attributes:
            if 'name' in attrib.key:
                names.append(attrib.value)

    return names


def get_directly_follows_single(name_list):
    """
    helper method for gets get_directly_follows_all: the "directly follows" relation for one single list of names
    :param name_list: single list of event names
    :return: list of all "directly follows" relations in the list
    """

    directly_follows = []
    if len(name_list) == 0:
        warnings.warn('The name list is empty!')
        return directly_follows

    last_index = len(name_list)
    for i in range(0, last_index - 1):
        directly_follows.append((name_list[i], name_list[i + 1]))

    return directly_follows


def get_directly_follows_all(traces: List[Trace]):
    """
    Part of step four of alpha algorithm: gets the "directly follows" relation for a list of lists that contains the
    event names
    :param traces: list of lists of event names (List[List[string]])
    :return: set of all
    directly-follows relations
    """

    name_lists = map_all_events_to_name(traces)

    directly_follows = []
    for n_list in name_lists:
        directly_follows = directly_follows + get_directly_follows_single(n_list)

    return set(directly_follows)


def get_inverse_directly_follows(traces):
    """
    computes the inverse of every "directly-follows"-tuple as support method for get_unrelated_relation
    :param traces: list of all traces in the log file
    :return: list of reversed "directly follows" tuples
    """

    directly_follows = get_directly_follows_all(traces)
    inverse_dir_fol = [tuple(reversed(t)) for t in directly_follows]

    return inverse_dir_fol


def get_causal_parallel_relation(traces):
    """
    part of step 4 of alpha algorithm: computes all parallel and causal relations of the tuples from the
    directly follows list
    :param traces: list of all traces from the log file
    :return: list of tuples of causal and parallel relations
    """

    directly_follows_list = list(get_directly_follows_all(traces))

    # remove all tuples that have their inverse version in the set
    parallel = []
    current_len = len(directly_follows_list)
    for i in range(0, current_len - 1):
        for j in range(i + 1, current_len):
            if reversed_tuples(directly_follows_list[i], directly_follows_list[j]):
                parallel.append(directly_follows_list[i])
                parallel.append(directly_follows_list[j])

    # causal relation is (directly-follows list) \ (parallel)
    causal = [t for t in directly_follows_list if t not in parallel]

    return set(causal), set(parallel)


def reversed_tuples(t1: tuple, t2: tuple):
    return set(t1) == set(t2)


def get_unrelated_relation(traces: List[Trace]):
    """
    part of step 4 of alpha algorithm: computes all "unrelated relations (#)" of the events in the list of traces
    :param traces: list of traces from the xes file
    :return: list of unrelated-relations tuples
    """

    name_set = get_event_names_as_set(traces)

    combinations = get_all_tuple_combinations(name_set)
    follows = get_directly_follows_all(traces)
    inverse_fol = get_inverse_directly_follows(traces)

    unrelated = [t for t in combinations if t not in follows and t not in inverse_fol]

    return unrelated


def get_disjoint_unrelated_sets(traces: List[Trace]):
    """
    calculates the disjoint unrelated tuples in the unrelated list, so that all elements in each set of the returned list
    have the relation "#" to each other
    :param traces: list of traces from the log file
    :return: list of sets, in which each element is unrelated to each other
    """

    unrelated_relation = get_unrelated_relation(traces)
    disjoint_sets = []

    for t in unrelated_relation:
        is_element = False

        for s in disjoint_sets:
            if t[0] in s and is_element_unrelated_with_set(t[1], s, unrelated_relation):
                s.add(t[1])
                is_element = True

        if not is_element:
            disjoint_sets.append({t[0], t[1]})

    return disjoint_sets


def is_element_unrelated_with_set(element, disjoint_set, unrelated_tuple_list):
    """
    computes whether an element has the "#" (unrelated) relation with every element in the disjoint set
    is helper method for get_disjoint_unrelated_set
    :param element: element in question
    :param disjoint_set: set of elements that are all pairwise unrelated to each other
    :param unrelated_tuple_list: list of tuples that contains all pairwise unrelated elements/events of the log file
    :return: True, if element is unrelated to every element from disjoint_set, false if otherwise
    """

    for el_dis in disjoint_set:
        for tup in unrelated_tuple_list:
            if (tup[1] == el_dis and tup[0] == element) or (tup[0] == el_dis and tup[1] == element):
                break
            if tup == unrelated_tuple_list[-1]:
                # if tup is the last tuple in the unrelated_tuple_list and no tuple has been found that contains
                # 'element' and 'el_dis' --> both elements are not unrelated and cannot be in the same "disjoint set"
                return False

    # element is unrelated to every other element in the disjoint set
    return True


def step_4(traces: List[Trace]):
    """
    step 4 and 5 of the alpha algorithm: calculate the relation defined in step 4 and get the maximum of them
    :param traces: list of traces defined in the log file
    :return: a list of relations as defined in step 4
    """

    causal, parallel = get_causal_parallel_relation(traces)
    set_directly_following = []  # List of Tuple containing two sets: [({'a'}, {'b', 'c'}), ({'d'}, {'e', 'f'})]
    set_directly_followed = []

    for fol_element in causal:
        is_element_following = False
        is_element_followed = False

        # calculate the list set_directly_following
        for following_element in set_directly_following:
            if fol_element[0] in following_element[0]:
                following_element[1].add(fol_element[1])  # all elements in following_element[1] are unrelated with each other
                is_element_following = True

        if not is_element_following:
            set_directly_following.append(({fol_element[0]}, {fol_element[1]}))

        # calculate the list set_directly_followed
        for followed_element in set_directly_followed:
            if fol_element[1] in followed_element[1]:
                followed_element[0].add(fol_element[0])
                is_element_followed = True

        if not is_element_followed:
            set_directly_followed.append(({fol_element[0]}, {fol_element[1]}))

    disjoint_unrelated = get_disjoint_unrelated_sets(traces)
    disjoint_unrelated = list(set(frozenset(item) for item in disjoint_unrelated))
    disjoint_unrelated = [set(item) for item in disjoint_unrelated]

    filtered_following_list_1 = [t for t in set_directly_following if len(t[1]) > 1]
    filtered_following_list_0 = [t for t in set_directly_following if len(t[1]) == 1]
    intersection_following = [intersection_unrelated_set(disjoint_unrelated, t, 1) for t in filtered_following_list_1]
    result_temp1 = [(filtered_following_list_1[i][0], s) for i in range(len(filtered_following_list_1)) for s in intersection_following[i]]

    filtered_followed = [t for t in set_directly_followed if len(t[0]) > 1]
    filtered_followed_list_0 = [t for t in set_directly_followed if len(t[0]) == 1]
    intersection_followed = [intersection_unrelated_set(disjoint_unrelated, t, 0) for t in filtered_followed]
    result_temp2 = [(s, filtered_followed[i][1]) for i in range(len(filtered_followed)) for s in
                    intersection_followed[i]]

    # if fist element of 2 tuples are unrelated with each other and all their "directly-follows" elements are the same,
    # they can be grouped as one --> step 5 of alpha algorithm

    result = filter_subset(result_temp1 + result_temp2 + filtered_followed_list_0 + filtered_following_list_0)
    return result


def filter_subset(tuple_list):
    """
    filters out all elements (tuples) in which both sets are already in another tuple as "subsets"
    :param tuple_list: list of tuples in question
    :return: filtered/simplified list of tuples
    """
    result = []

    for el in tuple_list:
        if any([r[0].issubset(el[0]) and r[1].issubset(el[1]) for r in result]):
            result = [r for r in result if not (r[0].issubset(el[0]) and r[1].issubset(el[1]))]
            result.append(el)
        if not any([el[0].issubset(r[0]) and el[1].issubset(r[1]) for r in result]):
            result.append(el)

    return result


def intersection_unrelated_set(disjoint_unrelated_set, following_relation, mode):
    """
    splits the set at index 'mode' of every tuple from 'following relation' according to 'disjoint_unrelated_set', so
    that every element form the split parts of the set are unrelated with each other.
    :param disjoint_unrelated_set: set of sets, in which all elements in one set are unrelated with each other
    :param following_relation: list of tuples of sets that have all grouped following-relation elements that exist
    :param mode: split the first set (0) or the second set (1) of each tuple
    :return: list of lists of sets, in which the set in question was split
    """
    # following relation: ({a, b}, {c, d, e})
    res = []
    fst_set = following_relation[mode]
    if len(fst_set) != 1:

        for dis_el in disjoint_unrelated_set:
            inters = fst_set.difference(dis_el, )
            if len(inters) != 0:
                if any([i.issubset(inters) for i in res]):
                    res = [r for r in res if not r.issubset(inters)]
                    res.append(inters)
                    break
                if not any([inters.issubset(i) for i in res]):
                    res.append(inters)
    return res


def in_same_disjoint_unrelated_set(element1, element2, disjoint_unrelated_list):
    """
    helper method to calculate whether element1 and element2 are unrelated
    :param element1: first element in question
    :param element2: second element in question
    :param disjoint_unrelated_list: list of sets, in which all elements are unrelated with each other
    :return: true, if both elements are unrelated, false otherwise
    """
    el1 = element1.pop()
    el2 = element2.pop()

    for s in disjoint_unrelated_list:
        if el1 in s and el2 in s:
            element2.add(el2)
            element1.add(el1)
            return True

    element2.add(el2)
    element1.add(el1)
    return False


def step_6_create_places(traces):
    """
    step 6 of alpha algorithm: creates all places
    :param traces: traces from the log file
    :return: list of traces including start and end
    """

    net_structure_set = step_4(traces)
    first_events, last_events = first_last_event_names(traces)

    # create Places from step_4, step_5
    places = [ds.Place(p[0], p[1]) for p in net_structure_set]

    # create start and end places
    start_place = ds.Place([], [ds.MyTransition(f_event) for f_event in first_events])
    end_place = ds.Place([ds.MyTransition(l_event) for l_event in last_events], [])
    places.append(start_place)
    places.append(end_place)

    return places


def step_7_create_edges(traces):
    """
    step 7 from the alpha algorithm: created all edges for the petri net
    :param traces: list of traces from the log file
    :return: list of all edges
    """

    # net_structure_set = step_4(traces)
    places_list = step_6_create_places(traces)

    edges = []
    for place in places_list:
        for source in place.in_list:
            e = ds.Edge(str(source), place)
            edges.append(e)
        for direction in place.out_list:
            e = ds.Edge(place, str(direction))
            edges.append(e)

    return edges


def main():
    (header, body) = prepare('log_data/billinstances.xes')
    traces = parse_body(body)
    event_list = map_all_events_to_name(traces)
    # event_names = get_event_names_as_set(traces)
    # all_names = all_events_to_name(traces)
    # (fist_event_names, last_event_names) = first_last_event_names(traces)
    directly_follows_all = get_directly_follows_all(traces)
    # inverse_dir_fol = get_inverse_directly_follows(traces)
    # name_combinations = get_all_tuple_combinations(get_event_names_as_set(traces))
    (causal, parallel) = get_causal_parallel_relation(traces)
    unrelated = get_unrelated_relation(traces)
    disjoint = get_disjoint_unrelated_sets(traces)
    add_to_unrelated_set = is_element_unrelated_with_set('c', {'a', 'b'},
                                                         [('a', 'b'), ('b', 'c'), ('e', 'a'), ('e', 'b'), ('e', 'c'),
                                                          ('a', 'c')])

    step_four = step_4(traces)
    edges = step_7_create_edges(traces)

    # print('all traces with event names: ' + str(event_list))
    # print('name combinations: ' + str(name_combinations))
    print('directly follows: ' + str(directly_follows_all))
    # print('inverse follows relations: ' + str(inverse_dir_fol))
    print('unrelated: ' + str(unrelated))
    print("causal: " + str(causal))
    print('parallel: ' + str(parallel))
    print('disjoint： ' + str(disjoint))
    print(step_four)
    for e in edges:
        print(str(e))


if __name__ == '__main__':
    main()
