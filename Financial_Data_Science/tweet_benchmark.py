# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:23:19 2022

@author: Richard
"""

import sqlite3 as lite
import pandas as pd 
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
#%%

sqliteConnection = lite.connect('TWEETS_Part2.db')
cursor = sqliteConnection.cursor()

ticker_list_query = """select  Ticker
           from ESGTWEETS
           Group BY Ticker"""

ticker_list = pd.read_sql_query(ticker_list_query,sqliteConnection)        

ticker_list = ticker_list['Ticker']

#%%   

# Clean the text
def CleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # Removing @mentions
    text = re.sub(r'#','',text) # Removing the '#' hashtag symbol 
    text = re.sub(r'RT[\s]+','',text) # Removing RT
    text = re.sub(r'https?:\/\/\S+', '', text) # Removing the hyperlink 
    text = re.sub('[,\.!?]', '', text)
    return text

# Create a function to get the subjectivity 
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity 

# Create a function to get the polarity 
def getPolarity(text):
    return TextBlob(text).sentiment.polarity 

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else: 
        return 'Positive'

#%%
tweet_query_front = """select  Tweets
           from ESGTWEETS WHERE Ticker == """
#%%

tickers_sentiment_analysis = pd.DataFrame(columns = ['ticker', 'number of tweets', 'posiive tweets percentage', 'negative tweets percentage'])

#%%

benchmark_tickers = []

ticlers_num_tweets = []

tickers_positive_tweets_per = []

tickers_negative_tweets_per = []


for ticker in ticker_list:

    tweet_query = tweet_query_front + "'" + ticker + "'"
    
    df = pd.read_sql_query(tweet_query,sqliteConnection) 
    
    if df.shape[0] < 10:
        continue
    
    ticker_num_tweets = df.shape[0]
    
    df['Tweets'] = df['Tweets'].apply(CleanTxt)

    # Create two new columns 
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)

    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    # Get the percentage of positive tweets 

    positive_tweets = df[df.Analysis == 'Positive']
    positive_tweets = positive_tweets['Tweets']

    # Get the percentage of negative tweets 

    negative_tweets = df[df.Analysis == 'Negative']
    negative_tweets = negative_tweets['Tweets']

    ticker_positive_tweets_per = round(positive_tweets.shape[0]/df.shape[0] , 2)

    ticker_negative_tweets_per = round(negative_tweets.shape[0]/df.shape[0] , 2)
    
    tickers_positive_tweets_per.append(ticker_positive_tweets_per)
    
    tickers_negative_tweets_per.append(ticker_negative_tweets_per)

    ticlers_num_tweets.append(ticker_num_tweets)
    
    benchmark_tickers.append(ticker)

tickers_sentiment_analysis['ticker'] = benchmark_tickers
    
tickers_sentiment_analysis['number of tweets'] = ticlers_num_tweets
    
tickers_sentiment_analysis['posiive tweets percentage'] = tickers_positive_tweets_per
    
tickers_sentiment_analysis['negative tweets percentage'] = tickers_negative_tweets_per



#%%

def social_media_influ_multi(sentiment_per_diff):
    
    social_media_influ_multi = np.sin((sentiment_per_diff+1)*np.pi/4)
    
    return social_media_influ_multi

#%%
plt.scatter(tickers_sentiment_analysis['negative tweets percentage'], tickers_sentiment_analysis['posiive tweets percentage'])
plt.xlabel('negative tweets percentage')
plt.ylabel('positive tweets percentage')
plt.title('positive VS. negative')
plt.show()


# from the plot we decide our model 
# for those has a positive percentage lower than 80% or negative percentage lower than 40%: normal
# for those has a positive percentage higher than 80%: leading
# for those has a negative percentage higher than 40%: lagging

#%%

tickers_sentiment_analysis['sentiment difference'] = tickers_sentiment_analysis['posiive tweets percentage'] - tickers_sentiment_analysis['negative tweets percentage']

#%%



tickers_sentiment_analysis['social media influence multiplier'] = social_media_influ_multi(tickers_sentiment_analysis['sentiment difference'])
plt.scatter(tickers_sentiment_analysis['sentiment difference'], tickers_sentiment_analysis['social media influence multiplier'])
plt.xlabel('sentiment difference')
plt.ylabel('social media influence multiplier')
plt.title('Benchmark Companies')
plt.show()

#%%
tickers_sentiment_analysis.to_csv("benchmark tickers sentiment analysis.csv", index=False)


