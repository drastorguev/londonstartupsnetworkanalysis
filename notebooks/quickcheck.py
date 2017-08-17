import networkx as nx
import json, time
from pymongo import MongoClient

V3=nx.Graph()

client = MongoClient('mongodb://localhost:27017/')
db = client.dissertation

twitterprofile = ['https://twitter.com/danstuart', 'https://twitter.com/polkaspots', 'http://twitter.com/#!/colinhayhurst', 'http://twitter.com/swimgeek', 'https://twitter.com/PshyMorphic', 'https://twitter.com/phpeach', 'http://twitter.com/mickhagen', 'https://twitter.com/#!/jibly']

for eachprofile in twitterprofile:
    recordexists = db.twitterlargenetwork.find({'twitterprofilename': str(eachprofile.split("/")[-1])})
    for eachfollower in recordexists[0]['followers']:
        V3.add_edge(recordexists[0]['twitterprofileid'],eachfollower)

print "done"

from networkx.readwrite import json_graph

testing = json_graph.node_link_data(V3)
testing['links'] = [{'source': testing['nodes'][link['source']]['id'], 'target': testing['nodes'][link['target']]['id']} for link in testing['links']]

targetjson = json.loads(json.dumps(testing))
del targetjson["directed"]
del targetjson["graph"]
del targetjson["multigraph"]

with open('largenextworkdata.json', 'w') as f:
  json.dump(targetjson, f)
