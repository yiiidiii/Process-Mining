import unittest
from alpha_miner import main as am, datastructures as ds
import xes_parser.main as xp


class TestAlphaMiner(unittest.TestCase):

    def test_l1(self):
        # Transitions:
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        correct_trans_list = [trans_a, trans_b, trans_c, trans_d, trans_e]
        correct_trans_names = ['a', 'b', 'c', 'd', 'e']
        # places:
        place_start = ds.Place([], [trans_a])
        place_a_eb = ds.Place([trans_a], [trans_e, trans_b])
        place_a_ec = ds.Place([trans_a], [trans_e, trans_c])
        place_eb_d = ds.Place([trans_e, trans_b], [trans_d])
        place_ec_d = ds.Place([trans_e, trans_c], [trans_d])
        place_end = ds.Place([trans_d], [])
        correct_place_list = [place_start, place_a_eb, place_a_ec, place_eb_d, place_ec_d, place_end]
        # correct edges
        correct_edges = [ds.Edge(trans_a, place_a_eb), ds.Edge(trans_a, place_a_ec),
                         ds.Edge(place_a_eb, trans_e), ds.Edge(place_a_eb, trans_b), ds.Edge(place_a_ec, trans_c),
                         ds.Edge(place_a_ec, trans_e), ds.Edge(trans_e, place_eb_d), ds.Edge(trans_b, place_eb_d),
                         ds.Edge(place_eb_d, trans_d), ds.Edge(trans_e, place_ec_d), ds.Edge(trans_c, place_ec_d),
                         ds.Edge(place_ec_d, trans_d), ds.Edge(place_start, trans_a), ds.Edge(trans_d, place_end)]

        # test results
        test_transitions, test_places, test_edges = run_miner('log_data/L1.xes')

        # assertions
        self.assertEqual(len(correct_trans_names), len(test_transitions), 'number of transition is not correct!')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct!')
        self.assertEqual(len(correct_place_list), len(test_places), 'number of places not correct')
        self.assertCountEqual(test_transitions, correct_trans_names)
        for p in correct_place_list:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')

    def test_bill(self):
        # correct_transitions
        trans_deliver = ds.MyTransition('deliver bill')
        trans_print = ds.MyTransition('print bill')
        trans_write = ds.MyTransition('write bill')
        correct_transitions = [trans_write, trans_deliver, trans_print]
        correct_transitions_names = map(lambda t: t.name, correct_transitions)

        # correct places
        place_pr_del = ds.Place([trans_print], [trans_deliver])
        place_wr_pr = ds.Place([trans_write], [trans_print])
        place_start = ds.Place([], [trans_write])
        place_end = ds.Place([trans_deliver], [])
        correct_places = [place_start, place_end, place_wr_pr, place_pr_del]

        # correct edges
        correct_edges = [ds.Edge(trans_print, place_pr_del), ds.Edge(place_pr_del, trans_deliver),
                         ds.Edge(trans_write, place_wr_pr), ds.Edge(place_wr_pr, trans_print),
                         ds.Edge(place_start, trans_write), ds.Edge(trans_deliver, place_end)]

        # test results
        test_transitions, test_places, test_edges = run_miner('log_data/billinstances.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct.')
        self.assertEqual(len(correct_places), len(test_places), 'number of places not correct.')
        self.assertCountEqual(test_transitions, correct_transitions_names)
        for p in correct_places:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')

    def test_poster(self):
        # correct transitions
        trans_deliver = ds.MyTransition('deliver poster')
        trans_print = ds.MyTransition('print poster')
        trans_receive = ds.MyTransition('receive order and photo')
        trans_design = ds.MyTransition('design photo poster')
        correct_transitions = [trans_deliver, trans_print, trans_design, trans_receive]
        correct_transitions_names = map(lambda t: t.name, correct_transitions)

        # correct places =
        p_print_deliver = ds.Place([trans_print], [trans_deliver])
        p_design_print = ds.Place([trans_design], [trans_print])
        p_receive_design = ds.Place([trans_receive], [trans_design])
        p_start = ds.Place([], [trans_receive])
        p_end = ds.Place([trans_deliver], [])
        correct_places = [p_end, p_start, p_receive_design, p_design_print, p_print_deliver]

        # correct edges
        correct_edges = [ds.Edge(trans_print, p_print_deliver), ds.Edge(p_print_deliver, trans_deliver),
                         ds.Edge(trans_receive, p_receive_design), ds.Edge(p_receive_design, trans_design),
                         ds.Edge(trans_design, p_design_print), ds.Edge(p_design_print, trans_print),
                         ds.Edge(p_start, trans_receive), ds.Edge(trans_deliver, p_end)]

        # test results
        test_transitions, test_places, test_edges = run_miner('log_data/posterinstances.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct.')
        self.assertEqual(len(correct_places), len(test_places), 'number of places not correct!')
        self.assertCountEqual(test_transitions, correct_transitions_names)
        for p in correct_places:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')


def run_miner(path_to_log_file):
    """
    prepares data and runs miner
    :param path_to_log_file: path to the XES log file
    :return: all event names as set, places from step 6, edges from step 7
    """
    (header, body) = am.prepare(path_to_log_file)
    traces = am.parse_body(body)
    event_names_llist = am.filtered_traces_list(traces)
    event_names_set = am.step_1_get_event_names_as_set(traces)
    first, last = am.step_2_3_first_last_event_names(event_names_llist)
    step_4_5_relations = am.step_4_5(event_names_set, event_names_llist)
    step_6_places = am.step_6_create_places(step_4_5_relations, first, last)
    step_7_edges = am.step_7_create_edges(step_6_places)

    return event_names_set, step_6_places, step_7_edges
