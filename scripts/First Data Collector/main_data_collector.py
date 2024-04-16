import requests
import json
from datetime import datetime, timezone
from langdetect import detect
import time


keywords = 'call of duty lag '

def twitter_analyzer(keywords, count):

    #URL and token
    twitter_bearer_token = ""
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    #Parameters to query
    headers = {'Authorization': 'Bearer {}'.format(twitter_bearer_token),}
    query_params = {'query': keywords+'(-is:retweet)',
                    'max_results' : count
                   }

    #Response treatment
    twitter_response = requests.get(url, headers=headers, data=query_params)
    tw_headers = twitter_response.headers
    
    available_requests = int(tw_headers.get('x-rate-limit-remaining', 0))
    limit_reset = int(tw_headers.get('x-rate-limit-reset', 0))
    max_requests = int(tw_headers.get('x-rate-limit-limit', 0))
    
    date = datetime.fromtimestamp(limit_reset, tz=timezone.utc)
    date_as_string = date.isoformat()
    
    results = json.loads(twitter_response.text)

    print("You still have {} available requests out of {} until {}".format(available_requests, max_requests, date_as_string))


    file = open(keywords+'.txt', 'x')
    file.write(keywords+'\n\n')
    for tweet in results.get('data', []):
        if (detect(tweet['text'])=='en'):
            file.write("%s\n\n" % tweet['text'])
    file.close()
    #check_available_requests(available_requests, date)
            
    
