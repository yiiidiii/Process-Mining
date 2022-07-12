import datetime
import csv
import lib.xes_parser.parser as xp
import lib.alpha_miner.miner as am
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
    event_list = am.filtered_traces_list(traces)  # this method, because it filters out all 'duplicate' events that are not the start of a lifecycle transition
    events_set = am.step_1_get_event_names_as_set(traces)

    events_occ_list = [{'event_name': str(event), 'occurrence': 0} for event in events_set]

    for events in event_list:
        # events = ['a', 'b', 'c']
        for d in events_occ_list:
            num = events.count(d.get('event_name'))
            d['occurrence'] = d.get('occurrence') + num

    events_occ_list = sorted(events_occ_list, key=lambda x: x['occurrence'], reverse=True)

    csv_path = open('static/statistics/event_number.csv', 'w')
    writer = csv.DictWriter(csv_path, fieldnames=events_occ_list[0].keys())
    writer.writeheader()
    for di in events_occ_list:
        writer.writerow(di)

    # return events_occ_list


def get_durations_of_traces(path_to_xes_file):
    """
    calculates the duration for each trace
    :param path_to_xes_file: path to the xes log file
    :return: trace with max duration, trace with min duration
    """
    (header, body) = xp.prepare(path_to_xes_file)
    traces = xp.parse_body(body)

    trace_duration_dict = [{'trace_name': next((x.value for x in t.attributes if x.key == 'concept:name'), None),
                            'duration': '0'} for t in traces]
    average_duration = datetime.timedelta(0)
    for trace in traces:
        # here, events are not filtered out because of lifecycle transitions, because the correct duration is until when an event is 'complete'
        trace_name = next((a.value for a in trace.attributes if a.key == 'concept:name'), None)
        time_start = next((a.value for a in trace.events[0].attributes if a.key == 'time:timestamp'), None)
        time_end = next((x.value for x in trace.events[-1].attributes if x.key == 'time:timestamp'), None)
        duration = parser.parse(time_end) - parser.parse(time_start)
        average_duration += duration

        # write duration into dict
        for d in trace_duration_dict:
            if d['trace_name'] == trace_name:
                d['duration'] = str(duration)

    average_duration = average_duration / len(trace_duration_dict)

    trace_duration_dict = sorted(trace_duration_dict, key=lambda x: x['duration'], reverse=True)

    # write into a csv file for further usage in the webserver
    csv_path = open('static/statistics/trace_durations.csv', 'w')
    writer = csv.DictWriter(csv_path, fieldnames=trace_duration_dict[0].keys())
    writer.writeheader()
    for di in trace_duration_dict:
        writer.writerow(di)

    return format_duration(average_duration)


def format_duration(duration):
    """
    formats the duration to HH:MM:SS (hours:minutes:seconds) to be consistent with the barchart
    :param duration: the duration as Timedelta object
    :return: correct format of duration as string
    """

    total_seconds = duration.seconds

    days = duration.days
    hours = (total_seconds // 3600) + (days * 24)
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f'{hours:d}:{minutes:02d}:{seconds:02d}'


def main():
    # print('number of events: ' + str(num_events_total('log_data/L1.xes')))
    # print('occurrences of all events: ' + str(num_events_total('log_data/L1.xes')))
    print('max and min duration of traces: ' + str(get_durations_of_traces('log_data/flyerinstances.xes')))


if __name__ == '__main__':
    main()
