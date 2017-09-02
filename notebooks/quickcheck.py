import networkx as nx
import json, time
from pymongo import MongoClient

V3=nx.Graph()

client = MongoClient('mongodb://localhost:27017/')
db = client.dissertation

twitterprofile = ['https://twitter.com/dannyking', 'http://twitter.com/#!/ninafaulhaber', 'http://twitter.com/#!/dougall', 'https://twitter.com/AneeshVarma', 'https://twitter.com/Agvesto', 'http://twitter.com/#!/LuisPabloPardo', 'http://twitter.com/#!/davidplans', 'http://www.twitter.com/luvaglio', 'http://www.twitter.com/alisisk', 'http://twitter.com/jonnycampbell', 'https://twitter.com/danbladen', 'https://twitter.com/charliecannell', 'https://twitter.com/tomcarra', 'http://twitter.com/#!/jaimefjorge', 'http://twitter.com/#!/caxaria', 'http://www.twitter.com/serenestudios', 'https://twitter.com/gshutler', 'https://twitter.com/billinghamj', 'http://twitter.com/#!/turi', 'http://twitter.com/#!/duediler', 'http://twitter.com/geoffwatts', 'https://twitter.com/kirill', 'https://twitter.com/mattjackrob', 'http://twitter.com/burgesg', 'https://twitter.com/murraymuzz', 'http://twitter.com/itsmarkchaffey', 'http://www.twitter.com/amfsd', 'https://twitter.com/simonprockter', 'http://twitter.com/#!/lmarsden', 'http://twitter.com/#!/gatosg', 'https://twitter.com/RMabey', 'https://twitter.com/pkoval', 'https://twitter.com/JustGo_official', 'http://twitter.com/#!/ChristianFaes', 'http://twitter.com/thait', 'http://twitter.com/#!/chrismorton', 'https://twitter.com/anilstocker', 'http://twitter.com/#!/oh_moore', 'http://twitter.com/#!/pakmee', 'http://twitter.com/#!/iHiD', 'http://twitter.com/#!/slowdive', 'http://twitter.com/#!/thomevincent', 'http://twitter.com/#!/stephenrapoport']

for eachprofile in twitterprofile:
    recordexists = db.twitterlargenetwork.find({'twitterprofilename': str(eachprofile.split("/")[-1])})
    print "working on " + str(eachprofile.split("/")[-1])
    for eachfollower in recordexists[0]['followers']:
        V3.add_edge(recordexists[0]['twitterprofileid'],eachfollower)

print "done adding edges"

from networkx.readwrite import json_graph

testing = json_graph.node_link_data(V3)
testing['links'] = [{'source': testing['nodes'][link['source']]['id'], 'target': testing['nodes'][link['target']]['id']} for link in testing['links']]

targetjson = json.loads(json.dumps(testing))
del targetjson["directed"]
del targetjson["graph"]
del targetjson["multigraph"]

with open('largenextworkdatayesfunding.json', 'w') as f:
  json.dump(targetjson, f)
