# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 15:05:03 2022

@author: Richard
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from math import e
import numpy as np
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import tweepy 
import seaborn as sns
import warnings
from textblob import TextBlob
import math
pi = math.pi

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

#%% Setting a benchmark for climate change scoring

sqliteConnection = lite.connect('implieds_temp_changes.db')
cursor = sqliteConnection.cursor()

temp_change_query = """select TICKER, TEMP_CHANGE
           from TEMPCHANGE
           """
df_temp_change = pd.read_sql_query(temp_change_query,sqliteConnection)        

#%% climate change scoring function

describe = df_temp_change['TEMP_CHANGE'].describe().round(2)

# 50 percentile implied temp rise is 1.98

# implied temp function 

def temp_rise_score(temprise):
    p_temprise = ((4-temprise)/2.7)*(e-1)
    temp_rise_score = np.log(p_temprise+1)*10
    return temp_rise_score    


#%% socail media influence multiplier function

def social_media_influ_multi(sentiment_per_diff):
    
    social_media_influ_multi = math.sin((sentiment_per_diff+1)*pi/4)
    
    return social_media_influ_multi


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

def final_scoring_model(ticker):
    
    driver = webdriver.Chrome()  

    driver.get('https://www.msci.com/research-and-insights/esg-ratings-corporate-search-tool');

    time.sleep(5) # take time for website to open

    search_box = driver.find_element(By.ID, '_esgratingsprofile_keywords')

    search_box.send_keys(ticker)

    time.sleep(5) # take time to let the search results to show up

    search_box.send_keys(Keys.ARROW_DOWN)

    search_box.send_keys(Keys.RETURN)

    time.sleep(3)
    
    # first, esg rating scoring based on the history rate of the company
    
    score_history = driver.find_element(by=By.XPATH, value = '//*[@id="_esgratingsprofile_esg-rating-history"]').text

    score_history = score_history.split('\n') # split the strings 

    most_previous_rate = score_history[0]

    latest_rate = score_history[4]
    
    # substract history rating infomation
    
    esg_rating_scale_list = driver.find_element(by=By.XPATH, value = '//*[@id="_esgratingsprofile_esg-rating-distribution"]').text

    esg_rating_scale_list = esg_rating_scale_list.split('\n')

    esg_rating_scales = []

    product = 0

    for i in range(0,7):
        
        num = re.findall(r"\d+", esg_rating_scale_list[i])
        
        num = float(num[0])
        
        product += num
           
        esg_rating_scales.append(product)
        
    # scoring is depend on the rating 

    def history_score(rating):
        
        if rating == "AAA":
            scale = 6
        elif rating == "AA":
            scale = 5
        elif rating == "A":
            scale = 4
        elif rating == "BBB":
            scale = 3
        elif rating == "BB":
            scale = 2
        elif rating == "B":
            scale = 1
        elif rating == "CCC":
            scale = 0
            
        score = esg_rating_scales[scale]
        
        return score  

    most_previous_score = history_score(most_previous_rate)

    latest_score = history_score(latest_rate)

    score_change = latest_score - most_previous_score

    # MSCI ESG Rating history data over the last five years or since records began.

    final_history_score = (latest_score + score_change/5)/10
    
    # momentum 
    
    
    # substract the industry info of the company
    
    company_industry = driver.find_element(by=By.XPATH, value = '//*[@id="_esgratingsprofile_esg-ratings-profile-graphs"]/div[1]/b').text

    company_industry = company_industry.replace(' industry','')

    industrymap = webdriver.Chrome()
    
    # open the industry materiality map website

    industrymap.get('https://www.msci.com/our-solutions/esg-investing/esg-ratings/materiality-map#');

    industry_search = industrymap.find_element(By.ID, 'search_input')
    
    # typing by every letter, get the best result
    
    for i in range (0,len(company_industry)):
        industry_search.send_keys(company_industry[i])
        try:
            search_dropdown = industrymap.find_element(by = By.XPATH, value = '//*[@id="subsector-search-dropdown"]/a[2]')
        except:
            break

    search_dropdown = industrymap.find_element(by = By.XPATH, value = '//*[@id="subsector-search-dropdown"]/a[1]')

    search_dropdown.click()
    
    xpath_start = '//*[@id="table-environment"]/tbody/tr['

    xpath_end = ']/td[2]/span'
    
    # E S G weights placed on the industry

    weights = []
    for i in range (1,14):
        num = str(i)
        xpath = xpath_start + num + xpath_end
        weight = industrymap.find_element(by=By.XPATH, value = xpath).text
        
        if weight == '':
            break
        weight = re.findall(r"\d+", weight)
        weight = float(weight[0])
        weights.append(weight)

    total_climate_weight = sum(weights)/100
    
    
    
    # decarbonization factor: whether it has a plan for future decarbonization
    
    decarbonization_target = driver.find_element(by=By.XPATH, value = '//*[@id="_esgratingsprofile_esg-company-transparency"]/div[7]/div[2]/div[1]/p[2]').text

    if decarbonization_target == 'NO':
        decarbonization_factor = 0
    elif decarbonization_target == 'YES':
        decarbonization_factor = 1

    # implied temperature rise score

    temp_rise = driver.find_element(by=By.CLASS_NAME, value = 'explanatory-sentence-temp').text

    temp_rise = re.findall(r"\d+\.?\d*", temp_rise)

    temp_rise_num = float(temp_rise[0])
    
    # as esg is a new topic, many companies may imply a high temp rise, but has a plan for it
    # for those imply a high temperature rise but has a plan, calculate their temp_rise_score as a 50 perncentile of the benchmark
   
    if temp_rise_num <= 2.51:
        climate_score = temp_rise_score(temp_rise_num)
    elif temp_rise_num > 2.51:
        if decarbonization_factor == 1:
            climate_score = temp_rise_score(2.51)
        elif decarbonization_factor == 0:
            climate_score = temp_rise_score(temp_rise_num)

    aggregate_esg_rating_score = final_history_score*(1 - total_climate_weight) + total_climate_weight*climate_score
    
    
    # social media net positive influnence multiplier
    
    # first, scrape tweets related with esg and the company
    
    search_topic = ticker + " AND esg"  # remove retweets 
    
    language="en"
    # Collect tweets:
    tweets = api.search_tweets(q = search_topic,
                                lang=language,
                                tweet_mode = 'extended',
                                count = 100
                                )
    df = pd.DataFrame([tweet.full_text for tweet in tweets],columns=['Tweets'])
   
    
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
    
    if df.shape[0] < 10:
        ticker_positive_tweets_per = 0
        ticker_negative_tweets_per = 0
        
    else:
        ticker_positive_tweets_per = round(positive_tweets.shape[0]/df.shape[0] , 4)

        ticker_negative_tweets_per = round(negative_tweets.shape[0]/df.shape[0] , 4)
        
    ticker_sentiment_per_diff = ticker_positive_tweets_per - ticker_negative_tweets_per
    
    ticker_socialmedia_multiplier = social_media_influ_multi(ticker_sentiment_per_diff)
    
    final_score = ticker_socialmedia_multiplier*aggregate_esg_rating_score
    
    final_score = final_score.round(2)
    
    aggregate_esg_rating_score = str(round(aggregate_esg_rating_score,2))
    ticker_socialmedia_multiplier = str(round(ticker_socialmedia_multiplier,2))
    final_score = str(round(final_score,2))
    print('The ESG base score of '+ ticker +' is: '+ aggregate_esg_rating_score)
    print('The social media influence multiplier of '+ ticker +' is: '+ ticker_socialmedia_multiplier)
    print('The Final score of '+ ticker +' is: '+final_score)

    
    return


#%% plots

plt.hist(df_temp_change['TEMP_CHANGE'], bins = 50)
plt.xlabel('Implied Temperature Rise (°C)')
plt.title('Benchmark Companies')
plt.show()
#%%

df_temp_change['TEMP_CHANGE_SCORE'] = temp_rise_score(df_temp_change['TEMP_CHANGE'])
plt.scatter(df_temp_change['TEMP_CHANGE'], df_temp_change['TEMP_CHANGE_SCORE'])
plt.xlabel('Implied Temperature Rise (°C)')
plt.ylabel('Climate Score')
plt.title('Benchmark Companies')
plt.show()


#%%


final_scoring_model('so')











