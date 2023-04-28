import nltk
import string

f = open("/Users/mehdibouchoucha/Desktop/merged_stream/delay2.txt", "r")

text = f.read()
stopwords = nltk.corpus.stopwords.words('english')
allWords = nltk.tokenize.TweetTokenizer().tokenize(text)
allWordDist = nltk.FreqDist(w.lower() for w in allWords if w.lower() not in stopwords and w.lower() not in [*string.punctuation])

for w in allWords:
    if w.lower() not in stopwords:
        #print(w)
        allWordExceptStopDist = nltk.FreqDist(w.lower())
mostCommon = allWordDist.most_common(50)

#for word, frequency in mostCommon:
#    print('%s: %d' % (word, frequency))

from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


tweets = [t.replace("://", "//") for t in nltk.corpus.twitter_samples.strings()]

from random import shuffle

def is_positive(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return sia.polarity_scores(tweet)["compound"] > 0

shuffle(tweets)
for tweet in tweets[:10]:
    print(">", is_positive(tweet), tweet)

positive_review_ids = nltk.corpus.twitter_samples.fileids(categories=["pos"])
negative_review_ids = nltk.corpus.twitter_samples.fileids(categories=["neg"])
all_review_ids = positive_review_ids + negative_review_ids


from statistics import mean

def is_positive(review_id: str) -> bool:
    """True if the average of all sentence compound scores is positive."""
    text = nltk.corpus.twitter_samples.raw(review_id)
    scores = [
        sia.polarity_scores(sentence)["compound"]
        for sentence in nltk.sent_tokenize(text)
    ]
    return mean(scores) > 0


shuffle(all_review_ids)
correct = 0
for review_id in all_review_ids:
    if is_positive(review_id):
        if review_id in positive_review_ids:
            correct += 1
    else:
        if review_id in negative_review_ids:
            correct += 1

print(F"{correct / len(all_review_ids):.2%} correct")