import requests
import json
import time
from py2cytoscape import util
import networkx as nx

HEADERS = {'Content-Type': 'application/json'}


class TestTools:

    def __init__(self, base_url, verbose=False):
        self.base_url = base_url
        self.verbose = verbose

    def post_job(self, path, d):
        url = self.base_url + path
        res = requests.post(url, data=d, headers=HEADERS)
        # TODO add check when service not there, res=empty...
        res_json = res.json()
        job_id = res_json.get('job_id')
        return job_id

    def get_result(self, job_id, sleep_interval=1, max_wait_intervals=0):
        status = 'queued'
        counter = 0
        while status == 'started' or status == 'queued':
            if counter > max_wait_intervals > 0:
                raise RuntimeError('Max wait inervalls surpassed')
            time.sleep(sleep_interval)
            jobs_json = self.get_jobs().json()
            for job in jobs_json:
                if job.get('job_id') == job_id:
                    status = job.get('status')
                    break
            if self.verbose:
                print(status)
            counter += 1

        if status == 'finished':
            return self.get_job(job_id)
        else:
            raise RuntimeError('Unexpected result status:' + status)

    def delete_job(self, job_id):
        # TODO does not work yet
        url = self.base_url + 'job' + '/' + job_id
        res = requests.delete(url)
        return res

    def get_jobs(self):
        url = self.base_url + 'jobs'
        res = requests.get(url)
        return res

    def get_job(self, job_id):
        url = self.base_url + 'jobs' + '/' + job_id
        res = requests.get(url)
        return res

    # Convenience methods
    def submit_network_to_service(self, path, cyjs):
        job_id = self.post_job(path, json.dumps(cyjs))
        return job_id

    # Static methods
    @staticmethod
    def delete_all_jobs():
        res = requests.delete()
        return res

    @staticmethod
    def cyjs_to_networkx(cyjs):
        return util.to_networkx(cyjs)

    @staticmethod
    def networkx_to_cyjs(g):
        return util.from_networkx(g)

    @staticmethod
    def is_isomorphic(g1, g2):
        # TODO node_match : callable
        if nx.faster_could_be_isomorphic(g1, g2):
            return nx.is_isomorphic(g1, g2)
        else:
            return False

