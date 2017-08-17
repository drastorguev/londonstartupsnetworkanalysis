import requests
from requests_oauthlib import OAuth1
import json, time
from details import *
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.dissertation


url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(item1, item2, item3, item4)
requests.get(url, auth=auth)

# twitterprofile = ['https://twitter.com/danstuart', 'https://twitter.com/polkaspots', 'http://twitter.com/#!/colinhayhurst', 'http://twitter.com/swimgeek', 'https://twitter.com/PshyMorphic', 'https://twitter.com/phpeach', 'http://twitter.com/mickhagen', 'https://twitter.com/#!/jibly']

twitterprofile = ['https://twitter.com/dannyking', 'http://twitter.com/#!/ninafaulhaber', 'http://twitter.com/#!/dougall', 'https://twitter.com/AneeshVarma', 'https://twitter.com/Agvesto', 'http://twitter.com/#!/LuisPabloPardo', 'http://twitter.com/#!/davidplans', 'http://www.twitter.com/luvaglio', 'http://www.twitter.com/alisisk', 'http://twitter.com/jonnycampbell', 'https://twitter.com/danbladen', 'https://twitter.com/charliecannell', 'https://twitter.com/tomcarra', 'http://twitter.com/#!/jaimefjorge', 'http://twitter.com/#!/caxaria', 'http://www.twitter.com/serenestudios', 'https://twitter.com/gshutler', 'https://twitter.com/billinghamj', 'http://twitter.com/#!/turi', 'http://twitter.com/#!/duediler', 'http://twitter.com/geoffwatts', 'https://twitter.com/kirill', 'https://twitter.com/mattjackrob', 'http://twitter.com/burgesg', 'https://twitter.com/murraymuzz', 'http://twitter.com/itsmarkchaffey', 'http://www.twitter.com/amfsd', 'https://twitter.com/simonprockter', 'http://twitter.com/#!/lmarsden', 'http://twitter.com/#!/gatosg', 'https://twitter.com/RMabey', 'https://twitter.com/pkoval', 'https://twitter.com/JustGo_official', 'http://twitter.com/#!/ChristianFaes', 'http://twitter.com/thait', 'http://twitter.com/#!/chrismorton', 'https://twitter.com/anilstocker', 'http://twitter.com/#!/oh_moore', 'http://twitter.com/#!/pakmee', 'http://twitter.com/#!/iHiD', 'http://twitter.com/#!/slowdive', 'http://twitter.com/#!/thomevincent', 'http://twitter.com/#!/stephenrapoport']

for eachprofile in twitterprofile:
    twitterid = requests.get('https://api.twitter.com/1.1/users/show.json?screen_name='+str(eachprofile.split("/")[-1]), auth=auth)
    actualtwitterid = twitterid.json()['id']
    time.sleep(70)
    recordexists = db.twitterlargenetwork.find({'twitterprofileid': actualtwitterid }).count()
    if recordexists > 0:
        print '--> Twitter profile has already been added to the database <--'
    else:
        allfollowers = []
        initialrequest = requests.get('https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name='+str(eachprofile.split("/")[-1])+'&count=5000', auth=auth)
        print "fetching data for "+eachprofile
        for eachtuser in initialrequest.json()['ids']:
            allfollowers.append(eachtuser)
        time.sleep(70)
        while initialrequest.json()['next_cursor'] != 0:
            print "fetching even more data for "+eachprofile
            initialrequest = requests.get('https://api.twitter.com/1.1/followers/ids.json?cursor='+initialrequest.json()['next_cursor_str']+'&screen_name='+str(eachprofile.split("/")[-1])+'&count=5000', auth=auth)
            for eachtuser in initialrequest.json()['ids']:
                allfollowers.append(eachtuser)
            time.sleep(70)
        collection = db.twitterlargenetwork.insert_one({
            'twitterprofilename': str(eachprofile.split("/")[-1]),
            'twitterprofileid': actualtwitterid,
            'followers': allfollowers
            })
        print '-->> added all followers to db for ' + str(eachprofile.split("/")[-1])
