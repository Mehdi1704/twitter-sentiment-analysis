# here i am importing important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline
plt.style.use("fivethirtyeight")
import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier
from sklearn.model_selection import train_test_split
from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS
from subprocess import check_output
import re

# here i am reading dataset
data = pd.read_csv("/Users/mehdibouchoucha/Desktop/twitter-sentiment-analysis-main/scripts/output.csv")
# here i am printing fisrt five line of dataset
data.head()

# here i am priting shape of dataset




# here i have decided to use only sentiment and text columns for doing sentiment analysis
data = data["text"]

# here i am printing first five line of my dataset
#data.head()

# here i am cleaning text column
def cleantxt(text):
    text= re.sub(r'@[A-Za-z0-9]+', '',text)# removed @mentions
    text= re.sub(r'#', '',text)# removed # symbol
    text = re.sub(r'RT[\s]+', '',text)# rmoved RT
    text = re.sub(r'https?:\/\/\s+', '',text)# removed the hyperlink
    text = re.sub(r':+', '',text)# removed : symbol
    text = re.sub(r'--+', '',text)# removed : symbol
    text = re.sub(r'http', '',text)
    return text
data = data.apply(cleantxt)

# here we are printing the first five line of cleaned data
data.head()

# here i am creating function to get subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
# here i am creating function to get polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity
# here i am creating two new column of subjectivity and polarity
#print(data.apply(getSubjectivity))
#print(data.apply(getPolarity))
'''
data["subjectivity"] = data.apply(getSubjectivity)
data["polarity"] = data.apply(getPolarity)


# here we are printing first five line of data after adding two new columns
data.head(10)

# here i am spliting dataset in train and test data
train,test = train_test_split(data,test_size=0.1)
# here i am removing neutral text
train = train[train.sentiment != "Neutral"]

# here i am training positive text
train_pos = train[train["sentiment"]=="positive"]
train_pos = train_pos["text"]
# here i am training neagative text
train_neg = train[train["sentiment"]=="negative"]
train_neg = train_neg["text"]
'''
train,test = train_test_split(data,test_size=0.1)
# here i am doing WordCloud visualization
allwords = ' '.join([twts for twts in data])
wordcloud = WordCloud(width=2500,
                      height=2000,stopwords=STOPWORDS,background_color="white",random_state=21
                     ).generate(allwords)
plt.figure(1,figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# here i am removing the hashtags, mentions, links and stopwords from the
#training set after doing visualisation
text = []
stopwords_set = set(stopwords.words("english"))

for index, row in train.iterrows():
    words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
    words_cleaned = [word for word in words_filtered
        if 'http' not in word
        and not word.startswith('@')
        and not word.startswith('#')
        and word != 'RT']
    words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
    text.append((words_without_stopwords, row.sentiment))

test_pos = test[ test['sentiment'] == 'Positive']
test_pos = test_pos['text']
test_neg = test[ test['sentiment'] == 'Negative']
test_neg = test_neg['text']

# Extracting word features
def get_words_in_text(text):
    all = []
    for (words, sentiment) in text:
        all.extend(words)
    return all

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    features = wordlist.keys()
    return features
w_features = get_word_features(get_words_in_text(text))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in w_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

 #  here i am Training the Naive Bayes classifier
training_set = nltk.classify.apply_features(extract_features,text)
classifier = nltk.NaiveBayesClassifier.train(training_set)

# here i have tried to measure how the classifier algorithm scored.
neg_cnt = 0
pos_cnt = 0
for obj in test_neg: 
    res =  classifier.classify(extract_features(obj.split()))
    if(res == 'Negative'): 
        neg_cnt = neg_cnt + 1
for obj in test_pos: 
    res =  classifier.classify(extract_features(obj.split()))
    if(res == 'Positive'): 
        pos_cnt = pos_cnt + 1
        
print('[Negative]: %s/%s '  % (len(test_neg),neg_cnt))        
print('[Positive]: %s/%s '  % (len(test_pos),pos_cnt))