from xes_parser.datastructure import *
from xes_parser.parser import *
import warnings
import alpha_miner.datastructures as ds


def filtered_traces_list(traces: List[Trace]):
    result_names = []
    for trace in traces:
        event_list_names = filter_lifecycle_start_events(trace.events)
        result_names.append(event_list_names)

    return result_names


def step_1_get_event_names_as_set(traces: List[Trace]):
    """
    Fist step of alpha algorithm: extracts all the names of all events without duplicates (as set)
    :param traces: list of traces
    :return: set of event names
    """

    all_events = []
    for trace in traces:
        all_events = list(all_events + trace.events)

    event_names = filter_lifecycle_start_events(all_events)

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


def step_2_3_first_last_event_names(all_events):
    """
    Second and third step of alpha algorithm: extracts the names of all first and last events in the list of traces
    :param all_events: list of lists of event names
    :return: set of names of the first events, list of names of last events
    """

    """# take the events from the trace objects
    all_events = []
    for trace in traces:
        all_events.append(trace.events)"""

    # take the first and last element from each event list
    first_events = set([event[0] for event in all_events])
    last_events = set([event[-1] for event in all_events])
    return first_events, last_events


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


def event_list_to_name_list(event_list):
    """
    helper method for map_all_events_to_name: for each event in event list, extract their names
    :param event_list: list of event objects
    :return: list of names (string)
    """

    names = []
    for event in event_list:
        event_name = next((a.value for a in event.attributes if a.key == 'concept:name'), None)
        names.append(event_name)

    return names


def filter_lifecycle_start_events(event_list):
    """
    helper method to filter out events that are not the start of a lifecycle
    :param event_list: list of event objects
    :return: list of names from events that are the start of a lifecycle
    """

    names = []
    for event in event_list:
        lifecycle_transition = next((a.value for a in event.attributes if a.key == 'start'), None)
        if lifecycle_transition == 'True':
            event_name = next((a.value for a in event.attributes if a.key == 'concept:name'), None)
            names.append(event_name)

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


def get_directly_follows_all(name_lists):
    """
    Part of step four of alpha algorithm: gets the "directly follows" relation for a list of lists that contains the
    event names
    :param name_lists: list of lists of event names (List[List[string]])
    :return: set of all directly-follows relations
    """

    directly_follows = []
    for n_list in name_lists:
        directly_follows = directly_follows + get_directly_follows_single(n_list)

    return set(directly_follows)


def get_inverse_directly_follows(event_names_llist):
    """
    computes the inverse of every "directly-follows"-tuple as support method for get_unrelated_relation
    :param event_names_llist: list of lists of event names
    :return: list of reversed "directly follows" tuples
    """

    directly_follows = get_directly_follows_all(event_names_llist)
    inverse_dir_fol = [tuple(reversed(t)) for t in directly_follows]

    return inverse_dir_fol


def get_causal_parallel_relation(event_names_llist):
    """
    part of step 4 of alpha algorithm: computes all parallel and causal relations of the tuples from the
    directly follows list
    :param event_names_llist: list of all traces from the log file
    :return: list of tuples of causal and parallel relations
    """

    directly_follows_set = list(get_directly_follows_all(event_names_llist))

    parallel = []

    # tuples with the pattern (x, x) are part of loop with length one --> add them to the list parallel
    for t in directly_follows_set:
        if t[0] == t[1]:
            parallel.append(t)

    # removes all tuples that are related with any of the loop-transitions
    to_be_removed = []
    # dir_fol_n = []
    for t in directly_follows_set:
        for p in parallel:
            if t[0] == p[0] or t[1] == p[0]:
                # break
                to_be_removed.append(t)
            # dir_fol_n.append(t)
    directly_follows_set = [t for t in directly_follows_set if t not in to_be_removed]

    # remove all tuples that have their inverse version in the set
    current_len = len(directly_follows_set)
    for i in range(0, current_len - 1):
        for j in range(i + 1, current_len):
            if set(directly_follows_set[i]) == set(directly_follows_set[j]):
                parallel.append(directly_follows_set[i])
                parallel.append(directly_follows_set[j])
        # loop of length 1: (x, x)
        """if directly_follows_set[i][0] == directly_follows_set[i][1]:
            parallel.append(directly_follows_set[i])
    if directly_follows_set[current_len - 1][0] == directly_follows_set[current_len - 1][1]:
        parallel.append(directly_follows_set[current_len - 1])"""

    # causal relation is (directly-follows list) \ (parallel)
    causal = [t for t in directly_follows_set if t not in parallel]

    return set(causal), set(parallel)


def reversed_tuples(t1: tuple, t2: tuple):
    return set(t1) == set(t2)


def get_unrelated_relation(event_names_set, event_names_llist):
    """
    part of step 4 of alpha algorithm: computes all "unrelated relations (#)" of the events in the list of traces
    :param event_names_llist: list of lists of event names
    :param event_names_set: all event names as set
    :return: list of unrelated-relations tuples
    """

    combinations = get_all_tuple_combinations(event_names_set)
    follows = get_directly_follows_all(event_names_llist)
    inverse_fol = get_inverse_directly_follows(event_names_llist)

    unrelated = [t for t in combinations if t not in follows and t not in inverse_fol]

    return unrelated


def get_disjoint_unrelated_sets(event_names_set, event_names_llist):
    """
    calculates the disjoint unrelated tuples in the unrelated list, so that all elements in each set of the returned list
    have the relation "#" to each other
    :param event_names_set, all event names as set
    :param event_names_llist: list of lists of event names
    :return: list of sets, in which each element is unrelated with each other
    """

    unrelated_relation = get_unrelated_relation(event_names_set, event_names_llist)
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


def step_4_5(event_names_set, event_name_llists):
    """
    step 4 and 5 of the alpha algorithm: calculate the relation defined in step 4 and get the maximum of them
    :param event_names_set: all events names as set
    :param event_name_llists: list of traces defined in the log file
    :return: a list of relations as defined in step 4
    """

    causal, parallel = get_causal_parallel_relation(event_name_llists)
    set_directly_following = []  # List of tuples containing two sets: [({'a'}, {'b', 'c'}), ({'d'}, {'e', 'f'})]
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

    disjoint_unrelated = get_disjoint_unrelated_sets(event_names_set, event_name_llists)
    disjoint_unrelated = list(set(frozenset(item) for item in disjoint_unrelated))
    disjoint_unrelated = [set(item) for item in disjoint_unrelated]

    filtered_following_list_1 = [t for t in set_directly_following if len(t[1]) > 1]
    filtered_following_list_0 = [t for t in set_directly_following if len(t[1]) == 1]
    intersection_following = [intersection_unrelated_set(disjoint_unrelated, t, 1) for t in filtered_following_list_1]
    result_temp1 = [(filtered_following_list_1[i][0], s) for i in range(len(filtered_following_list_1)) for s in intersection_following[i]]

    filtered_followed_list_1 = [t for t in set_directly_followed if len(t[0]) > 1]
    filtered_followed_list_0 = [t for t in set_directly_followed if len(t[0]) == 1]
    intersection_followed = [intersection_unrelated_set(disjoint_unrelated, t, 0) for t in filtered_followed_list_1]
    result_temp2 = [(s, filtered_followed_list_1[i][1]) for i in range(len(filtered_followed_list_1)) for s in intersection_followed[i]]

    # if fist element of 2 tuples are unrelated with each other and all their "directly-follows" elements are the same,
    # they can be grouped as one --> step 5 of alpha algorithm

    result = filter_subset(result_temp1 + filtered_following_list_0 + result_temp2 + filtered_followed_list_0)
    result = summarize_regarding_unrelated_set(result, disjoint_unrelated, 1)
    result = summarize_regarding_unrelated_set(result, disjoint_unrelated, 0)
    result = filter_subset(result)
    return result


def summarize_regarding_unrelated_set(tuple_list, disjoint_unrelated_set, mode):
    result = []
    if mode == 1:
        map_result = [False] * len(tuple_list)

        for i in range(len(tuple_list) - 1):
            for j in range(i + 1, len(tuple_list)):
                if tuple_list[i][0] == tuple_list[j][0] and any([set(tuple_list[i][1]).issubset(dis) and set(tuple_list[j][1]).issubset(dis) for dis in disjoint_unrelated_set]):
                    result.append((tuple_list[i][0], tuple_list[i][1].union(tuple_list[j][1])))
                    map_result[i] = True
                    map_result[j] = True

            # if element i could not be summarized with any other element
            if not map_result[i]:
                result.append(tuple_list[i])
                map_result[i] = True

        # for last element in list
        if not map_result[len(tuple_list) - 1]:
            result.append(tuple_list[len(tuple_list) - 1])

    if mode == 0:
        map_result = [False] * len(tuple_list)

        for i in range(len(tuple_list) - 1):
            for j in range(i + 1, len(tuple_list)):
                if tuple_list[i][1] == tuple_list[j][1] and any([set(tuple_list[i][0]).issubset(dis) and set(tuple_list[j][0]).issubset(dis) for dis in disjoint_unrelated_set]):
                    result.append((tuple_list[i][0].union(tuple_list[j][0]), tuple_list[i][1]))
                    map_result[i] = True
                    map_result[j] = True

            if not map_result[i]:
                result.append(tuple_list[i])
                map_result[i] = True

        if not map_result[len(tuple_list) - 1]:
            result.append(tuple_list[len(tuple_list) - 1])

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
            inters = fst_set.intersection(dis_el)
            if len(inters) != 0:
                if any([i.issubset(inters) for i in res]):
                    res = [r for r in res if not r.issubset(inters)]
                    res.append(inters)
                    continue
                if not any([inters.issubset(i) for i in res]):
                    res.append(inters)
    return res


"""def in_same_disjoint_unrelated_set(element1, element2, disjoint_unrelated_list):
    helper method to calculate whether element1 and element2 are unrelated
    :param element1: first element in question
    :param element2: second element in question
    :param disjoint_unrelated_list: list of sets, in which all elements are unrelated with each other
    :return: true, if both elements are unrelated, false otherwise
    
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
"""


def step_6_create_places(step_4_relations, first_event_names, last_event_names):
    """
    step 6 of alpha algorithm: creates all places
    :param last_event_names: names of all last events from the log file
    :param first_event_names: names of all first events from the log file
    :param step_4_relations: results from step 4
    :return: list of traces including start and end
    """

    # create Places from step_4, step_5
    places = [ds.Place(p[0], p[1]) for p in step_4_relations]

    # create start and end places
    start_place = ds.Place([], set([f_event for f_event in first_event_names]))
    end_place = ds.Place(set([l_event for l_event in last_event_names]), [])
    places.append(start_place)
    places.append(end_place)

    return places


def step_7_create_edges(places_list):
    """
    step 7 from the alpha algorithm: created all edges for the petri net
    :param places_list: list of places objects from step 6
    :return: list of all edges
    """

    edges = []
    for place in places_list:
        for source in place.in_list:
            e = ds.Edge(source, place)
            edges.append(e)
        for direction in place.out_list:
            e = ds.Edge(place, direction)
            edges.append(e)

    return edges


def alpha_miner(traces):
    event_names_llist = filtered_traces_list(traces)

    event_names_set = step_1_get_event_names_as_set(traces)
    first, last = step_2_3_first_last_event_names(event_names_llist)
    directly_follows = get_directly_follows_all(event_names_llist)
    unrelated = get_unrelated_relation(event_names_set, event_names_llist)
    causal, parallel = get_causal_parallel_relation(event_names_llist)

    step_4_5_relations = step_4_5(event_names_set, event_names_llist)
    step_6_places = step_6_create_places(step_4_5_relations, first, last)
    step_7_edges = step_7_create_edges(step_6_places)

    print('first: ' + str(first))
    print('last: ' + str(last))
    print('directly follows: ' + str(directly_follows))
    print('causal: ' + str(causal))
    print('unrelated: ' + str(unrelated))
    print('step 4, 5 relations' + str(step_4_5_relations))

    for p in step_6_places:
        print(str(p))
    for e in step_7_edges:
        print(str(e))


def main():
    (header, body) = prepare('log_data/L1.xes')
    traces = parse_body(body)
    alpha_miner(traces)


if __name__ == '__main__':
    main()
