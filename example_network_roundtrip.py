import json
import sys
import test_tools
import networkx as nx

BASE = 'http://192.168.59.103/v1/'
VERBOSE = True
SLEEP_INTERVAL = 0.5

if len(sys.argv) != 3:
    sys.exit(-1)

size = int(sys.argv[1])
path = sys.argv[2]

print(path)

g1 = nx.scale_free_graph(size)

cyjs1 = test_tools.TestTools.networkx_to_cyjs(g1)

tt = test_tools.TestTools(BASE, VERBOSE)

print(json.dumps(cyjs1))

# job_id = tt.post_job(path, json.dumps(cyjs1) )
job_id = tt.submit_network_to_service(path, cyjs1)
res = tt.get_result(job_id, SLEEP_INTERVAL, 10)

# print( res.json() )
cyjs2 = res.json()
print(json.dumps(cyjs2, indent=4))
# print( 'Result is at http://192.168.59.103/v1/jobs/' + job_id )

g2 = tt.cyjs_to_networkx(cyjs2)
print(nx.info(g2))
print(g2.nodes())
print(g2.edges())

print(tt.is_isomorphic(g1, g2))

# res = tt.delete_job( job_id )
# print(res)

# print(json.dumps(res.json(), indent=4))