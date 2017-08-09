import requests
from requests_oauthlib import OAuth1
import json, time
from details import *

import pickle


url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(item1, item2, item3, item4)
requests.get(url, auth=auth)

twitterprofile = ['jibly']

for eachprofile in twitterprofile:
    allfollowers = []
    initialrequest = requests.get('https://api.twitter.com/1.1/followers/list.json?cursor=-1&screen_name='+eachprofile+'&skip_status=true&include_user_entities=false&count=200', auth=auth)
    print "fetching data for "+eachprofile
    for eachtuser in initialrequest.json()['users']:
        allfollowers.append(eachtuser['screen_name'])
    while initialrequest.json()['next_cursor'] != 0:
        time.sleep(70)
        print "fetching even more data for "+eachprofile
        initialrequest = requests.get('https://api.twitter.com/1.1/followers/list.json?cursor='+initialrequest.json()['next_cursor_str']+'&screen_name='+eachprofile+'&skip_status=true&include_user_entities=false&count=200', auth=auth)
        for eachtuser in initialrequest.json()['users']:
            allfollowers.append(eachtuser['screen_name'])
    pickle.dump( allfollowers, open( eachprofile+".p", "wb" ) )
