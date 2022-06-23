from typing import List

import alpha_miner.main as am
import alpha_miner.datastructures as ds
import snakes.plugins
import graphviz

snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import (  # nets from loading plugins, found at runtime
    PetriNet,
    Transition,
    Variable,
    Value,
    Place
)


def create_net(path_to_xes):
    net = PetriNet('PetriNet')

    # create places
    (header, body) = am.prepare(path_to_xes)
    traces = am.parse_body(body)
    places = am.step_6_create_places(traces)

    for place in places:
        p = Place(place.name)
        net.add_place(p)

    # create transitions
    transitions = am.get_event_names_as_set(traces)
    for transition in transitions:
        t = Transition(str(transition))
        net.add_transition(t)

    # connect places with transitions
    edges = am.step_7_create_edges(traces)
    for edge in edges:
        if type(edge.source) is ds.Place:
            net.add_input(str(edge.source), str(edge.direction), Value(1))
        else:
            net.add_output(str(edge.direction), str(edge.source), Value(1))

    """net.add_input('1', 't1', Variable('x'))
    net.add_input('1', 't2', Value(1))
    net.add_output('2', 't1', Value(2))
    net.add_input('3', 't2', Value(1))
    net.add_output('2', 't2', Value(1))
    net.add_output('3', 't1', Value(2))"""

    return net


def draw_place(place, attr):
    attr['label'] = place.name.upper()
    attr['color'] = '#FA6D00'


def draw_transition(trans, attr):
    if str(trans.guard) == 'True':
        attr['label'] = trans.name
    else:
        attr['label'] = '%s\n%s' % (trans.name, trans.guard)


# --------------------- GRAPHVIZ ---------------------- #

def key(places_list: List[ds.Place] = None, transition_list: List[ds.MyTransition] = None):
    """
    helper method to create the key list --> rename the nodes to something that fits into nodes
    :param places_list: list of places
    :param transition_list: list of transitions
    :return: dictionary with key: actual name of transition/place, value: new name shown in petri net
    """
    if places_list is None:
        tr_legend = zip([str(t.name) for t in transition_list],
                        ['Trans ' + str(i) for i in list(range(len(transition_list)))])
        return dict(tr_legend)
    else:
        val_list = ['Place ' + str(i) for i in list(range(len(places_list)))]
        pl_legend = zip([str(p.name) for p in places_list if (p.name != 'start' and p.name != 'end')], val_list)
        pl_legend = list(pl_legend) + [('start', 'start'), ('end', 'end')]
        return dict(pl_legend)


def graphviz_net(path_to_xes):
    net = graphviz.Digraph('my Petri Net', filename='petri_net_vis/my_graphviz_net.gv', engine='neato')

    (header, body) = am.prepare(path_to_xes)
    traces = am.parse_body(body)
    places = am.step_6_create_places(traces)

    # create places
    net.attr('node', shape='circle', fixedsize='true', width='0.7')
    pl_legend = key(places, transition_list=None)
    for pl in pl_legend.values():
        net.node(str(pl))

    # create transitions
    obj_transitions = [ds.MyTransition(t) for t in am.get_event_names_as_set(traces)]
    trans_legend = key(places_list=None, transition_list=obj_transitions)
    net.attr('node', shape='box', style='filled', fillcolor='bisque')
    for t in trans_legend.values():
        net.node(str(t))

    # create edges
    edges = am.step_7_create_edges(traces)
    net.attr('edge', arrowsize='0.7', len='10')
    for e in edges:
        if type(e.source) is ds.Place:
            net.edge(str(pl_legend.get(str(e.source))), str(trans_legend.get(str(e.direction))))
        else:
            net.edge(str(trans_legend.get(str(e.source))), str(pl_legend.get(str(e.direction))))

    label = ''
    for pl in pl_legend.keys():
        label = label + f'{str(pl_legend.get(pl))}: {str(pl)}, \t'
    label = label + '\n'
    for tr in trans_legend.keys():
        label = label + f'{str(trans_legend.get(tr))}: {str(tr)}, \t'
    net.attr(overlap='false', fontsize='11', label=label)
    return net


def main():
    # net = create_net('log_data/L1.xes')
    # net.draw('petri_net_vis/my_net.png', place_attr=draw_place, trans_attr=draw_transition)
    net = graphviz_net('log_data/running-example.xml')
    net.view()


if __name__ == "__main__":
    main()
