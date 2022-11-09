# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 19:14:35 2022

@author: Richard
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3 as lite
import tweepy 
import seaborn as sns
import warnings

#%%
tickers = []

driver = webdriver.Chrome()  

driver.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies');

time.sleep(3)

ticker_xpath_start = '//*[@id="constituents"]/tbody/tr['

ticker_xpath_end = ']/td[1]/a'

for i in range (1,501):
    num = str(i)
    ticker_xpath = ticker_xpath_start + num + ticker_xpath_end
    ticker = driver.find_element(by=By.XPATH, value = ticker_xpath).text

    tickers.append(ticker)

driver.quit()
#%%
for ticker in tickers:
    print(type(ticker))



#%%

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

# Authentication
consumerKey = "dkxhDea0yKX30RGq4BJBhM3jM"
consumerSecret = "NzO22ktMunxjaDQ8lym24h2tlVhJ3n977kp3azGXvEhVl8Xrx0"
accessToken = "1509141367951441930-8TYzVjjnkBX3sb8vZwMPr6FGlQMolJ"
accessTokenSecret = "zqDwT3MnbScL6QAGO00h2GG5UPdNGI6xWZJ61Cv9sV3un"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

con = lite.connect('TWEETS_Part2.db')

with con:
    cur=con.cursor()
    cur.execute("DROP TABLE IF EXISTS ESGTWEETS") 
    cur.execute("CREATE TABLE ESGTWEETS(Ticker TEXT, Tweets TEXT)"); 
    
    for ticker in tickers:
        search_topic = ticker + " AND esg"  # remove retweets 
        print(search_topic)
        language="en"
        # Collect tweets:
        tweets = api.search_tweets(q = search_topic,
                                    lang=language,
                                    tweet_mode = 'extended',
                                    count = 100
                                    )
        for tweet in tweets:
            try: 
                cur.execute("INSERT OR IGNORE INTO ESGTWEETS VALUES(?, ?)",(ticker, tweet.full_text,))
            except lite.Error as error: 
                print(error)
        time.sleep(3)
        
con.commit()
con.close()



















