import unittest

import __init__
from alpha_miner import miner as am, datastructures as ds
import xes_parser.parser as xp


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
        test_transitions, test_places, test_edges = am.alpha_miner('static/test_files/xes_files/L1.xes')

        # assertions
        self.assertEqual(len(correct_trans_names), len(test_transitions), 'number of transition is not correct!')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct!')
        self.assertEqual(len(correct_place_list), len(test_places), 'number of places not correct')
        self.assertCountEqual(test_transitions, correct_trans_names)
        for p in correct_place_list:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')

    def test_l2(self):
        # Transitions:
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        trans_f = ds. MyTransition('f')
        correct_transitions = [trans_a, trans_b, trans_c, trans_d, trans_e, trans_f]
        correct_transition_names = map(lambda t: t.name, correct_transitions)

        # Places
        place_c_de = ds.Place([trans_c], [trans_d, trans_e])
        place_b_de = ds.Place([trans_b], [trans_d, trans_e])
        place_af_c = ds.Place([trans_a, trans_f], [trans_c])
        place_af_b = ds.Place([trans_a, trans_f], [trans_b])
        place_e_f = ds.Place([trans_e], [trans_f])
        place_start = ds.Place([], [trans_a])
        place_end = ds.Place([trans_d], [])
        correct_places = [place_start, place_end, place_e_f, place_af_b, place_af_c, place_b_de, place_c_de]

        # Edges
        correct_edges = [ds.Edge(place_start, trans_a), ds.Edge(trans_a, place_af_c), ds.Edge(trans_a, place_af_b), ds.Edge(place_af_c, trans_c),
                         ds.Edge(place_af_b, trans_b), ds.Edge(trans_f, place_af_b), ds.Edge(trans_f, place_af_c), ds.Edge(place_e_f, trans_f),
                         ds.Edge(trans_c, place_c_de), ds.Edge(trans_b, place_b_de), ds.Edge(trans_e, place_e_f), ds.Edge(place_c_de, trans_e),
                         ds.Edge(place_c_de, trans_d), ds.Edge(place_b_de, trans_e), ds.Edge(place_b_de, trans_d), ds.Edge(trans_d, place_end)]

        # test results
        test_transitions, test_places, test_edges = am.alpha_miner('static/test_files/xes_files/L2.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct.')
        self.assertEqual(len(correct_places), len(test_places), 'number of places not correct!')
        self.assertCountEqual(test_transitions, correct_transition_names)
        for p in correct_places:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')

    def test_l3(self):
        # transitions
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        trans_f = ds.MyTransition('f')
        trans_g = ds.MyTransition('g')
        correct_transitions = [trans_g, trans_e, trans_f, trans_d, trans_a, trans_b, trans_c]
        correct_transition_names_l3 = map(lambda t: t.name, correct_transitions)

        # Places
        place_e_fg = ds.Place([trans_e], [trans_f, trans_g])
        place_af_b = ds.Place([trans_a, trans_f], [trans_b])
        place_c_e = ds.Place([trans_c], [trans_e])
        place_d_e = ds.Place([trans_d], [trans_e])
        place_b_c = ds.Place([trans_b], [trans_c])
        place_b_d = ds.Place([trans_b], [trans_d])
        start = ds.Place([], [trans_a])
        end = ds.Place([trans_g], [])
        correct_places_l3 = [place_e_fg, place_af_b, place_b_c, place_b_d, place_d_e, place_c_e, start, end]

        # edges
        correct_edges_l3 = [ds.Edge(start, trans_a), ds.Edge(trans_a, place_af_b), ds.Edge(place_af_b, trans_b),
                            ds.Edge(trans_b, place_b_c), ds.Edge(place_b_c, trans_c), ds.Edge(trans_c, place_c_e), ds.Edge(place_c_e, trans_e),
                            ds.Edge(trans_b, place_b_d), ds.Edge(place_b_d, trans_d), ds.Edge(trans_d, place_d_e), ds.Edge(place_d_e, trans_e),
                            ds.Edge(trans_e, place_e_fg), ds.Edge(place_e_fg, trans_f), ds.Edge(trans_f, place_af_b),
                            ds.Edge(place_e_fg, trans_g), ds.Edge(trans_g, end)]

        # test results
        test_transitions_l3, test_places_l3, test_edges_l3 = am.alpha_miner('static/test_files/xes_files/L3.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_l3), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_l3), len(test_edges_l3), 'number of edges not correct.')
        self.assertEqual(len(correct_places_l3), len(test_places_l3), 'number of places not correct.')
        self.assertCountEqual(test_transitions_l3, correct_transition_names_l3)
        for p in correct_places_l3:
            self.assertIn(p, test_places_l3, f'did not find place {str(p)}!')
        for e in correct_edges_l3:
            self.assertIn(e, test_edges_l3, f'did not find edge {str(e)}!')

    def test_l4(self):
        # transitions
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        correct_transitions = [trans_a, trans_b, trans_c, trans_d, trans_e]
        correct_transition_names_l4 = map(lambda t: t.name, correct_transitions)

        # Places
        place_c_de = ds.Place([trans_c], [trans_d, trans_e])
        place_ab_c = ds.Place([trans_a, trans_b], [trans_c])
        start = ds.Place([], [trans_a, trans_b])
        end = ds.Place([trans_d, trans_e], [])
        correct_places_l4 = [place_ab_c, place_c_de, start, end]

        # Edges
        correct_edges_l4 = [ds.Edge(start, trans_a), ds.Edge(start, trans_b),
                            ds.Edge(trans_a, place_ab_c), ds.Edge(trans_b, place_ab_c),
                            ds.Edge(place_ab_c, trans_c), ds.Edge(trans_c, place_c_de),
                            ds.Edge(place_c_de, trans_d), ds.Edge(place_c_de, trans_e),
                            ds.Edge(trans_e, end), ds.Edge(trans_d, end)]

        # test results
        test_transitions_l4, test_places_l4, test_edges_l4 = am.alpha_miner('static/test_files/xes_files/L4.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_l4), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_l4), len(test_edges_l4), 'number of edges not correct.')
        self.assertEqual(len(correct_places_l4), len(test_places_l4), 'number of places not correct.')
        self.assertCountEqual(test_transitions_l4, correct_transition_names_l4)
        for p in correct_places_l4:
            self.assertIn(p, test_places_l4, f'did not find place {str(p)}!')
        for e in correct_edges_l4:
            self.assertIn(e, test_edges_l4, f'did not find edge {str(e)}!')

    def test_l5(self):
        # transitions
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        trans_f = ds.MyTransition('f')
        correct_transitions = [trans_a, trans_b, trans_c, trans_d, trans_e, trans_f]
        correct_transition_names_l5 = map(lambda t: t.name, correct_transitions)

        # PLaces
        place_b_cf = ds.Place([trans_b], [trans_c, trans_f])
        place_ad_b = ds.Place([trans_a, trans_d], [trans_b])
        place_e_f = ds.Place([trans_e], [trans_f])
        place_a_e = ds.Place([trans_a], [trans_e])
        place_c_d = ds.Place([trans_c], [trans_d])
        start = ds.Place([], [trans_a])
        end = ds.Place([trans_f], [])
        correct_places_l5 = [place_c_d, place_a_e, place_e_f, place_ad_b, place_b_cf, start, end]

        # edges
        correct_edges_l5 = [ds.Edge(start, trans_a),
                            ds.Edge(trans_a, place_a_e), ds.Edge(place_a_e, trans_e), ds.Edge(trans_e, place_e_f), ds.Edge(place_e_f, trans_f),
                            ds.Edge(trans_a, place_ad_b), ds.Edge(place_ad_b, trans_b), ds.Edge(trans_b, place_b_cf), ds.Edge(place_b_cf, trans_f),
                            ds.Edge(place_b_cf, trans_c), ds.Edge(trans_c, place_c_d), ds.Edge(place_c_d, trans_d), ds.Edge(trans_d, place_ad_b),
                            ds.Edge(trans_f, end)]

        # test results
        test_transitions_l5, test_places_l5, test_edges_l5 = am.alpha_miner('static/test_files/xes_files/L5.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_l5), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_l5), len(test_edges_l5), 'number of edges not correct.')
        self.assertEqual(len(correct_places_l5), len(test_places_l5), 'number of places not correct.')
        self.assertCountEqual(test_transitions_l5, correct_transition_names_l5)
        for p in correct_places_l5:
            self.assertIn(p, test_places_l5, f'did not find place {str(p)}!')
        for e in correct_edges_l5:
            self.assertIn(e, test_edges_l5, f'did not find edge {str(e)}!')

    def test_l6(self):
        # transitions
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        trans_d = ds.MyTransition('d')
        trans_e = ds.MyTransition('e')
        trans_f = ds.MyTransition('f')
        trans_g = ds.MyTransition('g')
        correct_transitions = [trans_a, trans_b, trans_c, trans_d, trans_e, trans_f, trans_g]
        correct_transition_names_l6 = map(lambda t: t.name, correct_transitions)

        # Places
        place_ef_g = ds.Place([trans_e, trans_f], [trans_g])
        place_cd_g = ds.Place([trans_c, trans_d], [trans_g])
        place_cf_g = ds.Place([trans_c, trans_f], [trans_g])
        place_de_g = ds.Place([trans_d, trans_e], [trans_g])
        place_b_d = ds.Place([trans_b], [trans_d])
        place_b_f = ds.Place([trans_b], [trans_f])
        place_a_c = ds.Place([trans_a], [trans_c])
        place_a_e = ds.Place([trans_a], [trans_e])
        start = ds.Place([], [trans_b, trans_a])
        end = ds.Place([trans_g], [])
        correct_places_l6 = [place_a_e, place_a_c, place_b_f, place_b_d, place_cf_g, place_ef_g, place_de_g, place_cd_g, start, end]

        # edges
        correct_edges_l6 = [ds.Edge(start, trans_b), ds.Edge(start, trans_a),
                            ds.Edge(trans_a, place_a_e), ds.Edge(trans_a, place_a_c), ds.Edge(trans_b, place_b_d), ds.Edge(trans_b, place_b_f),
                            ds.Edge(place_b_d, trans_d), ds.Edge(place_b_f, trans_f), ds.Edge(place_a_e, trans_e), ds.Edge(place_a_c, trans_c),
                            ds.Edge(trans_d, place_de_g), ds.Edge(trans_d, place_cd_g), ds.Edge(trans_f, place_ef_g), ds.Edge(trans_f, place_cf_g),
                            ds.Edge(trans_e, place_de_g), ds.Edge(trans_e, place_ef_g), ds.Edge(trans_c, place_cd_g), ds.Edge(trans_c, place_cf_g),
                            ds.Edge(place_de_g, trans_g), ds.Edge(place_ef_g, trans_g), ds.Edge(place_cd_g, trans_g), ds.Edge(place_cf_g, trans_g),
                            ds.Edge(trans_g, end)]

        # test results
        test_transitions_l6, test_places_l6, test_edges_l6 = am.alpha_miner('static/test_files/xes_files/L6.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_l6), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_l6), len(test_edges_l6), 'number of edges not correct.')
        self.assertEqual(len(correct_places_l6), len(test_places_l6), 'number of places not correct.')
        self.assertCountEqual(test_transitions_l6, correct_transition_names_l6)
        for p in correct_places_l6:
            self.assertIn(p, test_places_l6, f'did not find place {str(p)}!')
        for e in correct_edges_l6:
            self.assertIn(e, test_edges_l6, f'did not find edge {str(e)}!')

    def test_l7(self):
        # transitions
        trans_a = ds.MyTransition('a')
        trans_b = ds.MyTransition('b')
        trans_c = ds.MyTransition('c')
        correct_transitions = [trans_a, trans_b, trans_c]
        correct_transition_names_l7 = map(lambda t: t.name, correct_transitions)

        # places
        place_a_c = ds.Place([trans_a], [trans_c])
        start = ds.Place([], [trans_a])
        end = ds.Place([trans_c], [])
        correct_places_l7 = [place_a_c, start, end]

        # edges
        correct_edges_l7 = [ds.Edge(start, trans_a), ds.Edge(trans_a, place_a_c), ds.Edge(place_a_c, trans_c), ds.Edge(trans_c, end)]

        # test results
        test_transitions_l7, test_places_l7, test_edges_l7 = am.alpha_miner('static/test_files/xes_files/L7.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_l7), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_l7), len(test_edges_l7), 'number of edges not correct.')
        self.assertEqual(len(correct_places_l7), len(test_places_l7), 'number of places not correct.')
        self.assertCountEqual(test_transitions_l7, correct_transition_names_l7)
        for p in correct_places_l7:
            self.assertIn(p, test_places_l7, f'did not find place {str(p)}!')
        for e in correct_edges_l7:
            self.assertIn(e, test_edges_l7, f'did not find edge {str(e)}!')

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
        test_transitions, test_places, test_edges = am.alpha_miner('static/test_files/xes_files/billinstances.xes')

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
        test_transitions, test_places, test_edges = am.alpha_miner('static/test_files/xes_files/posterinstances.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges), len(test_edges), 'number of edges not correct.')
        self.assertEqual(len(correct_places), len(test_places), 'number of places not correct!')
        self.assertCountEqual(test_transitions, correct_transitions_names)
        for p in correct_places:
            self.assertIn(p, test_places, f'did not find place {str(p)}!')
        for e in correct_edges:
            self.assertIn(e, test_edges, f'did not find edge {str(e)}!')

    def test_flyer(self):
        # transitions
        trans_design = ds.MyTransition('design flyer')
        trans_receive = ds.MyTransition('receive flyer order')
        trans_send = ds.MyTransition('send draft to customer')
        trans_print = ds.MyTransition('print flyer')
        trans_deliver = ds.MyTransition('deliver flyer')
        correct_transitions = [trans_design, trans_receive, trans_send, trans_print, trans_deliver]
        correct_transition_names_flyer = map(lambda t: t.name, correct_transitions)

        # places
        place_send_print = ds.Place([trans_send], [trans_print])
        place_receive_design = ds.Place([trans_receive], [trans_design])
        place_print_deliver = ds.Place([trans_print], [trans_deliver])
        start = ds.Place([], [trans_receive])
        end = ds.Place([trans_deliver], [])
        correct_places_flyer = [place_send_print, place_receive_design, place_print_deliver, start, end]

        # edges
        correct_edges_fyler = [ds.Edge(start, trans_receive), ds.Edge(trans_receive, place_receive_design), ds.Edge(place_receive_design, trans_design),
                               ds.Edge(trans_send, place_send_print), ds.Edge(place_send_print, trans_print), ds.Edge(trans_print, place_print_deliver),
                               ds.Edge(place_print_deliver, trans_deliver), ds.Edge(trans_deliver, end)]

        # test results
        test_transitions_flyer, test_places_flyer, test_edges_flyer = am.alpha_miner('static/test_files/xes_files/flyerinstances.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_flyer), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_fyler), len(test_edges_flyer), 'number of edges not correct.')
        self.assertEqual(len(correct_places_flyer), len(test_places_flyer), 'number of places not correct!')
        self.assertCountEqual(test_transitions_flyer, correct_transition_names_flyer)
        for p in correct_places_flyer:
            self.assertIn(p, test_places_flyer, f'did not find place {str(p)}!')
        for e in correct_edges_fyler:
            self.assertIn(e, test_edges_flyer, f'did not find edge {str(e)}!')

    def test_running(self):
        # transitions
        trans_reinitiate = ds.MyTransition('reinitiate request')
        trans_register = ds.MyTransition('register request')
        trans_pay = ds.MyTransition('pay compensation')
        trans_ex_cas = ds.MyTransition('examine casually')
        trans_ex_tho = ds.MyTransition('examine thoroughly')
        trans_reject = ds.MyTransition('reject request')
        trans_check = ds.MyTransition('check ticket')
        trans_decide = ds.MyTransition('decide')
        correct_transitions = [trans_check, trans_decide, trans_reject, trans_pay, trans_ex_tho, trans_ex_cas, trans_reinitiate, trans_register]
        correct_transition_names_running = map(lambda t: t.name, correct_transitions)

        # places
        place_RegReini_CasuTho = ds.Place([trans_register, trans_reinitiate], [trans_ex_cas, trans_ex_tho])
        place_Dec_PayReiniRej = ds.Place([trans_decide], [trans_pay, trans_reinitiate, trans_reject])
        place_CasTho_Dec = ds.Place([trans_ex_cas, trans_ex_tho], [trans_decide])
        place_Check_Dec = ds.Place([trans_check], [trans_decide])
        place_RegReini_Check = ds.Place([trans_register, trans_reinitiate], [trans_check])
        start = ds.Place([], [trans_register])
        end = ds.Place([trans_reject, trans_pay], [])
        correct_places_running = [place_Check_Dec, place_RegReini_Check, place_Dec_PayReiniRej, place_CasTho_Dec, place_RegReini_CasuTho, start, end]

        # edges
        correct_edges_running = [ds.Edge(start, trans_register), ds.Edge(trans_register, place_RegReini_Check), ds.Edge(trans_register, place_RegReini_CasuTho),
                                 ds.Edge(place_RegReini_CasuTho, trans_ex_cas), ds.Edge(place_RegReini_CasuTho, trans_ex_tho),
                                 ds.Edge(trans_ex_cas, place_CasTho_Dec), ds.Edge(trans_ex_tho, place_CasTho_Dec), ds.Edge(place_CasTho_Dec, trans_decide),
                                 ds.Edge(place_RegReini_Check, trans_check), ds.Edge(trans_check, place_Check_Dec), ds.Edge(place_Check_Dec, trans_decide),
                                 ds.Edge(trans_decide, place_Dec_PayReiniRej), ds.Edge(place_Dec_PayReiniRej, trans_reinitiate),
                                 ds.Edge(trans_reinitiate, place_RegReini_Check), ds.Edge(trans_reinitiate, place_RegReini_CasuTho),
                                 ds.Edge(place_Dec_PayReiniRej, trans_reject), ds.Edge(place_Dec_PayReiniRej, trans_pay), ds.Edge(trans_pay, end),
                                 ds.Edge(trans_reject, end)]

        # test results
        test_transitions_running, test_places_running, test_edges_running = am.alpha_miner('static/test_files/xes_files/running-example.xes')

        # assertions
        self.assertEqual(len(correct_transitions), len(test_transitions_running), 'number of transitions not correct.')
        self.assertEqual(len(correct_edges_running), len(test_edges_running), 'number of edges not correct.')
        self.assertEqual(len(correct_places_running), len(test_places_running), 'number of places not correct!')
        self.assertCountEqual(test_transitions_running, correct_transition_names_running)
        for p in correct_places_running:
            self.assertIn(p, test_places_running, f'did not find place {str(p)}!')
        for e in correct_edges_running:
            self.assertIn(e, test_edges_running, f'did not find edge {str(e)}!')


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
