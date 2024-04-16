import requests
import json
from datetime import datetime, timezone
from langdetect import detect
import time
from itertools import combinations



# Here you can find the params you need to change to adapt the script to your machine
# TODO Change url, path and token
def init_params():

    global keywords_array
    global games_array
    global twitter_bearer_token
    global url
    global path

    keywords_array = ["lag ","ping (-pong) ","slow ","internetdown ","freeze (-cold) (-ice) ",
                    "packetloss ","internet ","poorservers ","delay ","internetsucks "]

    games_array = ["((call of duty) OR (cod)) ","league of legends ","((dota) OR (dota 2)) " ,"genshin impact ","warzone "]

    twitter_bearer_token = ""

    url = "https://api.twitter.com/2/tweets/search/recent"

    path = "/Users/mehdibouchoucha/Desktop/Projet/first_try/data/"

# API query function
def twitter_analyzer(keywords, count):

    headers = {'Authorization': 'Bearer {}'.format(twitter_bearer_token),}
    query_params = {'query': keywords+'(-is:retweet)',
                    'max_results' : count
                   }
    twitter_response = requests.get(url, headers=headers, data=query_params)
    tw_headers = twitter_response.headers
    available_requests = int(tw_headers.get('x-rate-limit-remaining', 0))
    limit_reset = int(tw_headers.get('x-rate-limit-reset', 0))
    max_requests = int(tw_headers.get('x-rate-limit-limit', 0))
    date = datetime.fromtimestamp(limit_reset, tz=timezone.utc)
    results = json.loads(twitter_response.text)

    print("You still have {} available requests out of {} until {}".format(available_requests, max_requests, date.isoformat()))
    file_writer(keywords, results)
    check_available_requests(available_requests, date)

    

# Writes in the keyword file
def file_writer(keywords, results):
    with open(path+keywords+'.txt', 'a') as file:
        for tweet in results.get('data', []):
            try:
                if (detect(tweet['text'])=='en'):
                    file.write("%s\n\n" % tweet['text'])
            except:
                continue
    file.close()
            
# Checks the request limit and sleeps for the necessary time to reset
def check_available_requests(available_requests, date):

    #arbitrary limit of 10 requests left
    if(available_requests < 10):
        # Get the difference between the current time and the reset time
        # Sleep during this delta time to wait for the reset (around 15min)
        # Adding 50 seconds for safety
        delta_time = (date - datetime.now(timezone.utc)).seconds + 50
        print("Going into sleep for {} seconds".format(delta_time))
        time.sleep(delta_time)
    
# Creates the  list of games + keywords we will use for the queries
def create_queries_combinations():

    global keywords_array
    combined_keywords = list(combinations(keywords_array, 2))
    all_combinations_list = []

    for pair in combined_keywords:
        keywords_array.append(pair[0] + pair[1])

    for game in games_array:
        for keyword in keywords_array:
            all_combinations_list.append(game+keyword)

    return all_combinations_list

# Main function that does the query for each keyword
def tweet_collector(keywords_list):

    for keyword in keywords_list:
        file = open(path+keyword+'.txt', 'x')
        total_size = len(keywords_list)
        element_position = keywords_list.index(keyword)+1
        for _ in range(10):
            twitter_analyzer(keyword, 100)
        print("File {} out of {} created and filled".format(element_position, total_size))
        

def main():

    init_params()
    keywords_list = create_queries_combinations()
    tweet_collector(keywords_list)

if __name__ == "__main__":
    main()
