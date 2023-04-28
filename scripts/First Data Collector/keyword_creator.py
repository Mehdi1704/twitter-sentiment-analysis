from itertools import combinations

keywords_array=["lag ","ping (-pong) ","slow ","internetdown ","freeze (-cold) (-ice) ",
                    "packetloss ","internet ","poorservers ","delay ","internetsucks "]

games_array=["(call of duty) OR (cod) ","league of legends ","(dota) OR (dota 2)","genshin impact ","warzone "]


# Creates all the combinations of keywords from the starting list and adds them to it
def create_keyword_combinations(keywords_array):
    combined_keywords = list(combinations(keywords_array, 2))
    for pair in combined_keywords:
        keywords_array.append(pair[0] + pair[1])
        
        
# Creates the final list of games + keywords we will use for the queries
def create_final_combination(games_array, keywords_array):
    create_keyword_combinations(keywords_array)
    all_combinations_list = []
    for game in games_array:
        for keyword in keywords_array:
            all_combinations_list.append(game+keyword)
    print(all_combinations_list)
    
