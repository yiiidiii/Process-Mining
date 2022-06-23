import xes_parser.main as xp
import alpha_miner.main as am
from dateutil import parser


def num_of_traces(path_to_xes_file):
    (header, body) = xp.prepare(path_to_xes_file)
    traces = xp.parse_body(body)
    return len(traces)


def num_events_total(path_to_xes_file):
    """
    calculates the total occurrence of each existing event in the log file
    :param path_to_xes_file: path to the log file
    :return: dictionary with event name (key) and occurrences (value)
    """
    (header, body) = xp.prepare(path_to_xes_file)
    traces = xp.parse_body(body)
    event_list = am.map_all_events_to_name(traces)
    events_set = am.get_event_names_as_set(traces)

    events_occ_dict = {str(e): 0 for e in events_set}

    for events in event_list:
        # events = ['a', 'b', 'c']
        for e in events_set:
            num = events.count(e)
            events_occ_dict[e] = events_occ_dict.get(e) + num

    return {k: v for k, v in sorted(events_occ_dict.items(), key=lambda item: item[1], reverse=True)}


def get_durations_of_traces(path_to_xes_file):
    """
    calculates the duration for each trace
    :param path_to_xes_file: path to the xes log file
    :return: trace with max duration, trace with min duration
    """
    (header, body) = xp.prepare(path_to_xes_file)
    traces = xp.parse_body(body)

    trace_duration_dict = {next((x.value for x in t.attributes if x.key == 'concept:name'), None): 0 for t in traces}
    for trace in traces:
        time_start = next((a.value for a in trace.events[0].attributes if a.key == 'time:timestamp'), None)
        time_end = next((x.value for x in trace.events[-1].attributes if x.key == 'time:timestamp'), None)
        duration = parser.parse(time_end) - parser.parse(time_start)
        trace_duration_dict[next((x.value for x in trace.attributes if x.key == 'concept:name'))] = str(duration)

    trace_duration_dict = {k: v for k, v in sorted(trace_duration_dict.items(), key=lambda item: item[1])}
    return (list(trace_duration_dict.keys())[0], list(trace_duration_dict.values())[0]), \
           (list(trace_duration_dict.keys())[-1], list(trace_duration_dict.values())[-1])


def duration_of_events(path_to_xes_file):
    (header, body) = xp.prepare(path_to_xes_file)
    traces = xp.parse_body(body)


def main():
    print('occurrences of all events: ' + str(num_events_total('log_data/L1.xes')))
    print('max and min duration of traces: ' + str(get_durations_of_traces('log_data/billinstances.xes')))


if __name__ == '__main__':
    main()
