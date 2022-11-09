# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 00:14:47 2022

@author: Richard
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re

def implied_temp_change_function(ticker):
    driver = webdriver.Chrome()  

    driver.get('https://www.msci.com/research-and-insights/esg-ratings-corporate-search-tool');

    time.sleep(5) # take time for website to open

    search_box = driver.find_element(By.ID, '_esgratingsprofile_keywords')

    search_box.send_keys(ticker)

    time.sleep(5) # take time to let the search results to show up

    search_box.send_keys(Keys.ARROW_DOWN)

    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)

    temp_rise = driver.find_element(by=By.CLASS_NAME, value = 'explanatory-sentence-temp').text

    temp_rise = re.findall(r"\d+\.?\d*", temp_rise)

    temp_rise_num = float(temp_rise[0])
    
    driver.quit()
    
    return temp_rise_num

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    