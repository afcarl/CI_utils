from flask.ext import restful
from py2cytoscape import util
from flask.ext.restful import reqparse
from jobs import q, job_list

# Lifetime of the results.
RESULT_TIME_TO_LIVE = 500000


class NetworkService1(restful.Resource):

    def __init__(self):
        self.__parser = reqparse.RequestParser()

    def post(self):
        """
        Create and submit a new graph analysis job in the queue.
        :return:
        """
        self.__parser.add_argument('elements', type=dict, help='Elements')
        self.__parser.add_argument('data', type=dict, help='Network Attr')
        graph = self.__parser.parse_args()

        # Send the time-consuming job to workers
        job = q.enqueue_call(func=self.calculate, args=(graph, {}), result_ttl=RESULT_TIME_TO_LIVE)
        job_list.append(job.get_id())

        result = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url': 'http://192.168.59.103/v1/jobs/' + job.get_id()
        }

        return result, 202

    def calculate(self, graph, params):
        pass


class Rt1(NetworkService1):
    def calculate(self, graph, params):
        nx_graph = util.to_networkx(graph)
        return util.from_networkx(nx_graph)