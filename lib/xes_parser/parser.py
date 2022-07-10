import string
import xml.etree.ElementTree as ET
from typing import Union
import warnings
# from dateutil import parser
import numpy as np

import run.__init__
from xes_parser import datastructure


def prepare(path_to_xes_file: string):
    """
    converts xes file into two xml-header and xml-body uploaded_files.
    :path_tp_xes_file: path to the xes file that should be converted (string)
    :return: tuple of path to the header.xml and body.xml that the xes file was split into
    """

    # read file
    file = open(path_to_xes_file, 'r')
    lines = file.readlines()
    file.close()

    path_header = 'xes_header.xml'
    path_body = 'xes_body.xml'
    new_file = open(path_header, 'w')
    xes_copy = open(path_body, 'w')
    xes_copy.write('<log>\n')

    first = False
    for line in lines:
        if '?xml' in line:
            new_file.write(line)
            # xes_copy.write(line)
        elif 'log' in line:
            new_file.write(line)
            # xes_copy.write(line)
        elif '<trace>' in line and not first:
            first = True
            xes_copy.write(line)
        elif '<trace>' not in line and not first:
            new_file.write(line)
        else:
            xes_copy.write(line)

    xes_copy.write('</log>\n')

    return path_header, path_body


def parse_header(path_to_header_xml: string):
    return NotImplemented


def parse_body(path_to_body_xml: string):
    """
    Generates trace and event objects according to the process in the xes file.
    :param path_to_body_xml: path to the file that contains the body part/trace information of the xes file
    :return: list of all trace objects from the xes-body file. 
    """

    tree = ET.parse(path_to_body_xml)
    root = tree.getroot()
    traces = list(root)

    # list of lists of events for each trace
    event_list = [list(trace) for trace in traces]

    # create Trace objects 
    for i in range(0, len(traces)):
        trace_attrib = []  # attributes of the trace traces[i]
        for j in event_list[i]:
            if len(j.attrib) > 0:
                trace_attrib.append(j)
        event_list[i] = difference(event_list[i], trace_attrib)

        # convert to Event objects
        event_list_n = []
        for e in event_list[i]:
            # here e (event) is just a list of strings/lines with the elements being the attributes --> convert
            # into Event objects
            e = parse_event(e)

            # event is of type None (start of lifecycle transition or no attributes) --> delete event from event list
            # of the trace
            if e is None:
                continue
            event_list_n.append(e)

        # create map of all types of lifecycle transitions
        life_cycle_types = event_list_n
        life_cycle_types = set(map(lambda event:
                               next((ev.value for ev in event.attributes if ev.key == 'lifecycle:transition'), None),
                               life_cycle_types))

        # handle life cycle transitions
        event_list_n = handle_life_cycles(event_list_n, life_cycle_types)

        # if event list is empty, the trace is not considered
        if len(event_list_n) == 0:
            break

        # convert elements of trace_attributes into Attribute objects and create trace object
        trace_attrib = [datastructure.Attribute(attr.get('key'), attr.get('value')) for attr in trace_attrib]
        traces[i] = datastructure.Trace(trace_attrib, event_list_n)

    return traces


def parse_event(event) -> Union[datastructure.Event, None]:
    """
    event in this case is only a list of strings, with each string representing an attribute line. This method
    converts the elements into Event object with the respective attributes
    :param event: list of attribute lines in string format
    :return: Event object or None, if event has no attributes
    """
    if len(event) == 0:
        return None

    attributes = []
    has_name = False
    for attr in event:
        key = attr.attrib.get('key')
        val = attr.attrib.get('value')
        # TODO: lifecycle transition, remove if statement
        # if 'lifecycle:transition' in key and 'start' in val:
        #     return None
        if 'concept:name' in key:
            has_name = True
        attributes.append(datastructure.Attribute(key, val))

    # create Event object
    if not has_name:
        warnings.warn('event has no name, it will be ignored by the miner!')
        return None
    event = datastructure.Event(attributes)
    return event


def handle_life_cycles(event_list, life_cycle_types):
    if len(life_cycle_types) == 1:
        for event in event_list:
            event.attributes.append(datastructure.Attribute('start', 'True'))
    else:
        for event in event_list:
            lifecycle_transition = next((a.value for a in event.attributes if a.key == 'lifecycle:transition'), None)
            if lifecycle_transition == 'start':
                event.attributes.append(datastructure.Attribute('start', 'True'))
            else:
                event.attributes.append(datastructure.Attribute('start', 'False'))
    return event_list


def difference(lst1, lst2):
    """
    helper method for extracting the attributes of a trace: computes the difference of two lists of ElementTree.Elements
    :param lst1: longer list (with trace attributes and events)
    :param lst2: shorter list (only trace attributes)
    :return: list with only events
    """
    # len(lst1) > len(lst2)
    a = lst1
    b = lst2
    mask = np.full((len(a)), True)
    for num in b:
        for i, num2 in enumerate(a):
            if num == num2 and mask[i]:
                mask[i] = False
                break

    result = []
    for j, m in enumerate(mask):
        if m:
            result.append(a[j])
    return result


def main():
    (header, body) = prepare('log_data/L1.xes')
    traces = parse_body(body)
    print(str(traces))


if __name__ == "__main__":
    main()
