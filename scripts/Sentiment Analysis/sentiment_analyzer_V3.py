import nltk
import pandas as pd
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import string


def cleantxt(text):
    text= re.sub(r'@[A-Za-z0-9]+', '',text)# removed @mentions
    text= re.sub(r'#', '',text)# removed # symbol
    text = re.sub(r'RT[\s]+', '',text)# rmoved RT
    text = re.sub(r'https?:\/\/\s+', '',text)# removed the hyperlink
    text = re.sub(r':+', '',text)# removed : symbol
    text = re.sub(r'--+', '',text)# removed : symbol
    text = re.sub(r'http', '',text)
    return text

def is_positive(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return SentimentIntensityAnalyzer().polarity_scores(tweet)["compound"] > 0

def is_neutral(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return SentimentIntensityAnalyzer().polarity_scores(tweet)["compound"] == 0

def is_negative(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return SentimentIntensityAnalyzer().polarity_scores(tweet)["compound"] < 0

def score_sentiment_analysis(filepath):
    score = 0
    data = pd.read_csv(filepath, on_bad_lines='skip')
    #data.to_csv('output.csv', mode = 'a', index=False, header=False)
    data = data["text"]

    for tweet in data:
        curr_score = SentimentIntensityAnalyzer().polarity_scores(tweet)["compound"]
        score += curr_score
        print("tweet: {}\n score: {}".format(tweet, curr_score))
    return score/len(data)


def most_commom_words(filepath):    
    f = open(filepath, "r")
    text = f.read()
    stopwords = nltk.corpus.stopwords.words('english')
    allWords = nltk.tokenize.TweetTokenizer().tokenize(text)
    allWordDist = nltk.FreqDist(w.lower() for w in allWords if w.lower() not in stopwords and w.lower() not in [*string.punctuation])

    for w in allWords:
        if w.lower() not in stopwords:
            allWordExceptStopDist = nltk.FreqDist(w.lower())
    mostCommon = allWordDist.most_common(50)
    return mostCommon

    

#print(most_commom_words("/Users/mehdibouchoucha/Desktop/cod.csv"))
#print(score_sentiment_analysis("/Users/mehdibouchoucha/Desktop/twitter-sentiment-analysis-main/output.csv"))

def most_common_in_file(file_list):
    with open("commonwords.txt", "x") as f:
        for file in file_list:
            print("writing file "+file)
            mostCommon = most_commom_words("/Users/mehdibouchoucha/Desktop/twitter-sentiment-analysis-main/sentiment_data/"+file+".txt")
            f.write("{"+file+"\n")
            for word, frequency in mostCommon:
                f.write('%s: %d \n' % (word, frequency))
            f.write("}\n")

file_list = [
    "cod",
    "delay", 
    "delay2",
    "dota", 
    "genshin",
    "internet", 
    "internet2",
    "lag", 
    "lag2",
    "lol", 
    "ping",
    "ping2", 
    "slow",
    "slow2",
    "warzone" 
    ]

