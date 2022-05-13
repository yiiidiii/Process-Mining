from hashlib import new
from multiprocessing import Event
import string
import xml.etree.ElementTree as ET

from trace import Trace
from event import Event
from dateutil import parser


def prepare(path_to_xes_file: string):
    """
    converts xes file into two xml-header and xml-body files.
    
    :path_to_xes_file: path to the xes file that should be converted (string)
    :return: tuple of path to the header.xml and body.xml that the xes file was split into
    """

    # read file
    file = open(path_to_xes_file, 'r')
    lines = file.readlines()
    file.close

    path_header = 'xes_parser/xes_header.xml'
    path_body = 'xes_parser/xes_body.xml'
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

    return (path_header, path_body)


def parse_body(path_to_header_xml: string, path_to_body_xml: string):
    """
    Generates trace and event objects according to the process in the xes file.
    :return: list of all trace objects from the xes-body file. 
    """
    tree = ET.parse(path_to_body_xml)
    root = tree.getroot()
    traces = list(root)
    
    # list of list of events for each trace 
    event_list = []
    for trace in traces:
        event_list.append(list(trace))
    
    # print(event_list[0][0].attrib.keys())
    
    # create Trace objects 
    for i in range(0, len(traces)):
        trace_id = event_list[i].pop(0)

        # convert to Event objects
        event_list_n = []
        for e in event_list[i]:
            e = parse_event(e)
            event_list_n.append(e)
        
        traces[i] = Trace(trace_id.attrib.get('value'), event_list_n)

    return traces


def parse_event(event) -> Event:

    activity = None
    resource = None
    timestamp = None
    transition = None

    for attr in event:
        key = attr.attrib.get('key')
        val = attr.attrib.get('value')
        if 'name' in key:
            activity = val
        elif 'resource' in key:
            resource = val 
        elif 'time' in key:
            timestamp = parser.parse(val)
        elif 'transition' in key:
            transition = val
    
    # create Event object
    event = Event(activity, timestamp, resource, transition)
    return event        


def main():
    (header, body) = prepare('log_data/L1.xes')
    traces = parse_body(header, body)
    print(traces)


if __name__ == "__main__":
    main()