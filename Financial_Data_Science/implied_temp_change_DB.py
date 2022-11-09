# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 00:35:08 2022

@author: Richard
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3 as lite
from implied_temp_change import implied_temp_change_function

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
con = lite.connect('implieds_temp_changes.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS TEMPCHANGE")
cur.execute("CREATE TABLE TEMPCHANGE(TICKER text, TEMP_CHANGE float)")

for ticker in tickers:
    try:
        implied_temp_change = implied_temp_change_function(ticker)
        
        cur.execute("INSERT OR IGNORE INTO TEMPCHANGE VALUES(?, ?)", (ticker, implied_temp_change))
    except:
        continue
       
con.commit()
con.close()
