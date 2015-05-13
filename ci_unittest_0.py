import unittest
import test_tools
import networkx as nx

BASE = 'http://192.168.59.103/v1/'
VERBOSE = True
SLEEP_INTERVAL = 1


class TestCIMethods(unittest.TestCase):

    def setUp(self):
        print("setUp")
        tt = test_tools.TestTools(BASE, VERBOSE)
        self.g1 = nx.scale_free_graph(10)
        cyjs1 = test_tools.TestTools.networkx_to_cyjs(self.g1)
        job_id = tt.submit_network_to_service('network_service_1/rt1', cyjs1)
        res = tt.get_result(job_id, SLEEP_INTERVAL, 10)
        cyjs2 = res.json()
        self.g2 = tt.cyjs_to_networkx( cyjs2 )

    def tearDown(self):
        print("tearDown")

    def test_is_isomorphic(self):
        self.assertTrue(test_tools.TestTools.is_isomorphic( self.g1, self.g2))

    def test_has_expected_number_of_nodes(self):
        self.assertTrue(len(self.g2.nodes())==10)


if __name__ == '__main__':
    unittest.main()