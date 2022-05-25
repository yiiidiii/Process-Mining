from xes_parser.datastructure import *
from xes_parser.main import *
import warnings


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

    return set(event_names)


def first_last_event_names(traces: List[Trace]):
    """
    Second and third step of alpha algorithm: extracts the names of all first and last events in the list of traces
    :param traces: list of traces in the log file
    :return: list of names of the first events, list of names of last events
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
    helper method for event_list_to_name_list: maps all the events in the lists of events to their respective names
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
    for each event in event list, extract their names
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


def get_directly_follows_all(name_lists):
    """
    Part of step four of alpha algorithm: gets the "directly follows" relation for a list of lists that contains the
    event names
    :param name_lists: list of lists of event names (List[List[string]])
    :return: set of all
    directly-follows relations
    """

    directly_follows = []
    for n_list in name_lists:
        directly_follows = directly_follows + get_directly_follows_single(n_list)

    return set(directly_follows)


def get_causal_parallel_relation(directly_follows_list: List[tuple]):
    # remove all tuples that have their inverse version in the set
    # convert to set so that order does not matter and comparison is easier
    # tuples_to_sets = list(map(lambda t: set(t), directly_follows_list))

    parallel = []
    current_len = len(directly_follows_list)
    for i in range(0, current_len - 1):
        for j in range(i + 1, current_len):
            if reversed_tuples(directly_follows_list[i], directly_follows_list[j]):
                parallel.append(directly_follows_list[i])
                parallel.append(directly_follows_list[j])

    causal = [t for t in directly_follows_list if t not in parallel]

    return causal, parallel


def reversed_tuples(t1: tuple, t2: tuple):
    return set(t1) == set(t2)


def main():
    (header, body) = prepare('log_data/L1.xml')
    traces = parse_body(body)
    # event_names = get_event_names_as_set(traces)
    # all_names = all_events_to_name(traces)
    # (fist_event_names, last_event_names) = first_last_event_names(traces)
    directly_follows_all = get_directly_follows_all(map_all_events_to_name(traces))
    (causal, parallel) = get_causal_parallel_relation(list(directly_follows_all))
    print(directly_follows_all)
    print(causal)


if __name__ == '__main__':
    main()
