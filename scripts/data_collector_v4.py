import requests
import json
from datetime import datetime, timezone
from langdetect import detect
import time
import csv
import pandas as pd
import copy



# Here you can find the params you need to change to adapt the script to your machine
# TODO Change url and token
def init_params():

    global first_array
    global second_array
    global big_array
    global twitter_bearer_token
    global url
    global dictionnary
    global nb_of_queries


    twitter_bearer_token = ""

    url = "https://api.twitter.com/2/tweets/search/recent"
    
    # nb of queries you want per keyword. A query will look for 100 tweets --> 100 queries = 10k tweets per query 
    nb_of_queries = 100


    first_array = ["((call of duty) OR (cod)) ","league of legends ","((dota) OR (dota 2)) " 
                ,"twitch ","((stream) OR (streaming)) ", "game ", "internet ", "connection "]

    
    second_array = ["((lag) OR (lag spikes) OR (lag issues)) ","ping (-pong) ","slow (-movement) "
                    ,"freeze (-cold) (-ice) ","delay ", "bad ", "issues ", "unplayable "]


    cod_array = ['((call of duty) OR (cod)) ((lag) OR (lag spikes) OR (lag issues)) ', 
    '((call of duty) OR (cod)) ping (-pong) ', '((call of duty) OR (cod)) slow (-movement) ', 
    '((call of duty) OR (cod)) freeze (-cold) (-ice) ', '((call of duty) OR (cod)) delay ', 
    '((call of duty) OR (cod)) bad ', '((call of duty) OR (cod)) issues ', 
    '((call of duty) OR (cod)) unplayable ']
    lol_array = [
    'league of legends ((lag) OR (lag spikes) OR (lag issues)) ', 
    'league of legends ping (-pong) ', 'league of legends slow (-movement) ', 'league of legends freeze (-cold) (-ice) ', 
    'league of legends delay ', 'league of legends bad ', 'league of legends issues ', 'league of legends unplayable ']
    dota_array = [
    '((dota) OR (dota 2)) ((lag) OR (lag spikes) OR (lag issues)) ', '((dota) OR (dota 2)) ping (-pong) ', 
    '((dota) OR (dota 2)) slow (-movement) ', '((dota) OR (dota 2)) freeze (-cold) (-ice) ', '((dota) OR (dota 2)) delay ', 
    '((dota) OR (dota 2)) bad ', '((dota) OR (dota 2)) issues ', '((dota) OR (dota 2)) unplayable ']
    twitch_array = [
    'twitch ((lag) OR (lag spikes) OR (lag issues)) ', 'twitch ping (-pong) ', 'twitch slow (-movement) ', 
    'twitch freeze (-cold) (-ice) ', 'twitch delay ', 'twitch bad ', 'twitch issues ', 'twitch unplayable ']
    stream_array = [
    '((stream) OR (streaming)) ((lag) OR (lag spikes) OR (lag issues)) ', '((stream) OR (streaming)) ping (-pong) ', 
    '((stream) OR (streaming)) slow (-movement) ', '((stream) OR (streaming)) freeze (-cold) (-ice) ', 
    '((stream) OR (streaming)) delay ', '((stream) OR (streaming)) bad ', '((stream) OR (streaming)) issues ', 
    '((stream) OR (streaming)) unplayable ']
    game_array = [
    'game ((lag) OR (lag spikes) OR (lag issues)) ', 'game ping (-pong) ', 
    'game slow (-movement) ', 'game freeze (-cold) (-ice) ', 'game delay ', 'game bad ', 'game issues ', 'game unplayable ']
    internet_array = [
    'internet ((lag) OR (lag spikes) OR (lag issues)) ', 'internet ping (-pong) ', 'internet slow (-movement) ', 
    'internet freeze (-cold) (-ice) ', 'internet delay ', 'internet bad ', 'internet issues ', 'internet unplayable ']
    connection_array = [
    'connection ((lag) OR (lag spikes) OR (lag issues)) ', 'connection ping (-pong) ', 'connection slow (-movement) ', 
    'connection freeze (-cold) (-ice) ', 'connection delay ', 'connection bad ', 'connection issues ', 'connection unplayable ']

    big_array = [cod_array, lol_array, dota_array, twitch_array, stream_array, game_array, internet_array, connection_array]

    dictionnary = dict()

# API query function
def twitter_analyzer(keywords, count, next_token):
    
    headers = {'Authorization': 'Bearer {}'.format(twitter_bearer_token),}
    query_params = {'query': keywords+'(-is:retweet)',
                    'max_results' : count,
                    'tweet.fields' : 'created_at,author_id'
                    
                    }
    query_params_with_next_token = {'query': keywords+'(-is:retweet)',
                    'max_results' : count,
                    'pagination_token' : next_token,
                    'tweet.fields' : 'created_at,author_id'
                    
                   }
    if(next_token==""):
        twitter_response = requests.get(url, headers=headers, data=query_params)
    else:
        twitter_response = requests.get(url, headers=headers, data=query_params_with_next_token)
    tw_headers = twitter_response.headers
    available_requests = int(tw_headers.get('x-rate-limit-remaining', 0))
    limit_reset = int(tw_headers.get('x-rate-limit-reset', 0))
    max_requests = int(tw_headers.get('x-rate-limit-limit', 0))
    date = datetime.fromtimestamp(limit_reset, tz=timezone.utc)
    results = json.loads(twitter_response.text)
    try:
        next_token = results.get("meta").get("next_token")
        print("next token: " + next_token)
    except:
        next_token = "end"
        print("no next token")

    print("You still have {} available requests out of {} until {}".format(available_requests, max_requests, date.isoformat()))
    #df = pd.DataFrame(results['data'])
    #df.to_csv('response_python.csv', mode='a')
    
    #csv_writer(keywords, results)
    check_available_requests(available_requests, date)
    dictionnary.update(results)
    return next_token

    

# Writes in the keyword file
def clean_list(data_list):
    for tweet in data_list:
        try:
            if not (detect(tweet['text'])=='en'):
                data_list.pop(data_list.index(tweet))
        except:
            data_list.pop(data_list.index(tweet))
    return data_list
    
            

def csv_writer(keywords, results):
    print("csv written")
    # Define the structure of the data
    header = ['id','author_id','created_at','edit_history_tweet_ids','text']
    with open(keywords+'.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for tweet in results.get('data', []):
            try:
                if (detect(tweet['text'])=='en'):
                    #tweet_data = [tweet['text'], "test", "tweet['author_id']"]
                    writer.writerows(tweet)
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

    
    all_combinations_list = []

    for first in first_array:
        for second in second_array:
            all_combinations_list.append(first+second)

    return all_combinations_list

# Main function that does the query for each keyword
def tweet_collector(big_list):

    for little_list in big_list:
        #file = open(path+keyword+'.txt', 'x')
        total_size = len(big_list)
        element_position = str(big_list.index(little_list)+1)
        next_token = ""
        final_list = list()
        for element in little_list:
            for _ in range(nb_of_queries):
                if not (next_token=="end"):
                    next_token = twitter_analyzer(element, 100, next_token)
                    try: 
                        final_list.extend(dictionnary["data"])
                    except:
                        print("couldn't extend dictionnary")
                    dictionnary.clear()
            final_list = clean_list(final_list)
        df = pd.DataFrame(final_list)
        df.to_csv("file_"+element_position+'.csv', mode='a')
        print("File {} out of {} created and filled".format(element_position, total_size))
        

def main():

    init_params()
    tweet_collector(big_array)

if __name__ == "__main__":
    main()

