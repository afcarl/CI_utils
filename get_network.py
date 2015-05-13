import json
import sys
import test_tools
import networkx as nx

BASE = 'http://192.168.59.103/v1/'
VERBOSE = True
SLEEP_INTERVAL = 0.5

if len(sys.argv) != 2:
    sys.exit(-1)

arg1 = sys.argv[1]

tt = test_tools.TestTools(BASE, VERBOSE)

res = tt.get_jobs()

print(json.dumps(res.json(), indent=4))

job_id = tt.post_job(arg1, None)
res = tt.get_result(job_id, SLEEP_INTERVAL, 10)

# print( res.json() )
cyjs = res.json()
print(json.dumps(cyjs, indent=4))
print('Result is at http://192.168.59.103/v1/jobs/' + job_id)

g = tt.cyjs_to_networkx(cyjs)
print(nx.info(g))
print(g.nodes())
print(g.edges())

g2 = tt.cyjs_to_networkx(cyjs)

print(tt.is_isomorphic(g, g2))

res = tt.delete_job(job_id)
print(res)

# print(json.dumps(res.json(), indent=4))