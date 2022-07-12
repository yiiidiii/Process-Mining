import os.path
from typing import List

import run.__init__
import alpha_miner.miner as am
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


# --------------------- GRAPHVIZ ----------------------

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
    file_name = os.path.basename(path_to_xes)
    file_name = file_name.replace('.xes', '')
    net = graphviz.Digraph('my Petri Net', filename=f'static/test_files/png_files/{file_name}', engine='neato', format='pdf')

    # preparation
    (header, body) = am.prepare(path_to_xes)
    traces = am.parse_body(body)
    event_names_llist = am.filtered_traces_list(traces)
    event_names_set = am.step_1_get_event_names_as_set(traces)
    first, last = am.step_2_3_first_last_event_names(event_names_llist)
    step_4_5_relations = am.step_4_5(event_names_set, event_names_llist)
    step_6_places = am.step_6_create_places(step_4_5_relations, first, last)
    step_7_edges = am.step_7_create_edges(step_6_places)

    # create places
    net.attr('node', shape='circle', fixedsize='true', width='0.7', margin='1')
    pl_legend = key(step_6_places, transition_list=None)
    for pl in pl_legend.values():
        net.node(str(pl))

    # create transitions
    obj_transitions = [ds.MyTransition(t) for t in am.step_1_get_event_names_as_set(traces)]
    trans_legend = key(places_list=None, transition_list=obj_transitions)
    net.attr('node', shape='box', style='filled', fillcolor='lightpink2', margin='1')
    for t in trans_legend.values():
        net.node(str(t))

    # create edges
    net.attr('edge', arrowsize='0.7', len='1')
    for e in step_7_edges:
        if type(e.source) is ds.Place:
            net.edge(str(pl_legend.get(str(e.source))), str(trans_legend.get(str(e.direction))))
        else:
            net.edge(str(trans_legend.get(str(e.source))), str(pl_legend.get(str(e.direction))))

    # generate graph label
    label1 = f'petri net generated from file {file_name}.xes'
    label2 = f'{label1}\n'
    for pl in pl_legend.keys():
        label2 = label2 + f'{str(pl_legend.get(pl)) :<}: {str(pl)}, \n'
    label2 = label2 + '\n'
    for tr in trans_legend.keys():
        label2 = label2 + f'{str(trans_legend.get(tr))}: {str(tr)}, \n'

    net.attr(overlap='scale', fontsize='11', label=label2)
    net.render(f'static/test_files/svg_files/petri_net', cleanup=True, format='pdf')
    # net.view()

    net.attr(overlap='scale', fontsize='11', label=label1)
    return net, pl_legend, trans_legend


def main():
    net, pl, trans = graphviz_net('log_data/running-example.xes')
    net.view()


if __name__ == "__main__":
    main()
