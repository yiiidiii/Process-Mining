import string
import xml.etree.ElementTree as ET
from dateutil import parser

from xes_parser import datastructure


def prepare(path_to_xes_file: string):
    """
    converts xes file into two xml-header and xml-body files.
    
    :path_to_xes_file: path to the xes file that should be converted (string)
    :return: tuple of path to the header.xml and body.xml that the xes file was split into
    """

    # read file
    file = open(path_to_xes_file, 'r')
    lines = file.readlines()
    file.close()

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

    return path_header, path_body


def parse_header(path_to_header_xml: string):
    return NotImplemented


def parse_body(path_to_body_xml: string):
    """
    Generates trace and event objects according to the process in the xes file.
    :param path_to_body_xml: path to the xml/xes file that contains the body part/trace information of the log
    :return: list of all trace objects from the xes-body file. 
    """

    tree = ET.parse(path_to_body_xml)
    root = tree.getroot()
    traces = list(root)
    
    # list of list of events for each trace 
    event_list = []
    for trace in traces:
        event_list.append(list(trace))
    
    # create Trace objects 
    for i in range(0, len(traces)):
        trace_id = event_list[i].pop(0)

        # convert to Event objects
        event_list_n = []
        for e in event_list[i]:
            # here e (event) is just a list of strings/lines with the elements being the attributes --> conversion
            # into Event objects
            e = parse_event(e)

            # event objects has no attributes --> delete event from event list of the trace
            if len(e.attributes) == 0:
                break

            event_list_n.append(e)

        # if event list is empty, the trace is not considered
        if len(event_list_n) == 0:
            break
        
        traces[i] = datastructure.Trace(trace_id.attrib.get('value'), event_list_n)

    return traces


def parse_event(event) -> datastructure.Event:
    """
    event in this case is only a list of strings, with each string representing an attribute line. This method
    converts the elements into Event object with the respective attributes
    :param event: list of attribute lines in string format
    :return: Event object
    """

    attributes = []

    for attr in event:
        key = attr.attrib.get('key')
        val = attr.attrib.get('value')
        attributes.append(datastructure.Attribute(key, val))
    
    # create Event object
    event = datastructure.Event(attributes)
    return event        


def main():
    (header, body) = prepare('log_data/L1.xml')
    traces = parse_body(body)
    print(traces)


if __name__ == "__main__":
    main()
