# -*- coding: utf-8 -*-
"""
Created on 2021/04/14 
@author: Bill
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions
from selenium.common.exceptions import NoSuchElementException 
import time
import pandas as pd
import sys


print("program start")

prices = {"itemFilter":[],
          "item":[],
          "manu":[],
          "descr":[],
          "stockQty":[],
          "firmName":[],
          "link":[],
          "quantity":[],
          "price":[]}

price_df = pd.DataFrame.from_dict(prices)

fileName = ""
saveFileName = open("saveFileName.txt","r")
for file in saveFileName:
    fileName = file.replace('\n', '')
    break
saveFileName.close()

options = EdgeOptions()
options.use_chromium = True

f = open("item_list.txt", "r")
for itemNo in f:
    itemFilter = itemNo.replace('\n', '').replace("\\", "%5C").replace("/", "%2F").replace(" ", "%20")
    #driver = webdriver.Chrome()
    driver = Edge(options = options)
    

    url= "http://www.findchips.com/search/"+itemFilter+"?currency=USD"
    driver.get(url)
    time.sleep(8)
    driver.find_element_by_css_selector('#filterInStockInput').send_keys( "1" + Keys.ENTER)
    time.sleep(2)
    
    #txtFileName = itemFilter + "UC3842BD1R2G.json"
    firmList = driver.find_elements_by_css_selector("div.distributor-results")
    print("program running")

    count = 0
    for firm in firmList:
        #print(firm.get_attribute("id"))
        firmName = ""
        href = ""
        try:
            firmName = firm.find_element_by_css_selector('h3.distributor-title a')
            href = firmName.get_attribute('href')
        except NoSuchElementException:
            firmName = ""
            href = ""
            print("NoSuchElementException")
        except:
            # print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error")
            raise
        
        learnMore = firm.find_elements_by_css_selector('table tr:not([style*="display: none;"]) td ul.price-list li a')
        for learn in learnMore:
            time.sleep(1)
            learn.click()
        
        
        trs = firm.find_elements_by_css_selector('table tr:not([style*="display: none;"])')
        
        for tr in trs:
            
            # 料號
            itemLi = tr.find_elements_by_css_selector('td.td-part.first div.part-name a')
            for item in itemLi:
                itemLink = item.text
                break
            
            # 製造商
            manuTd = tr.find_elements_by_css_selector('td.td-mfg span')
            for manufact in manuTd:
                manu = manufact.text
                break
            
            # 說明
            descTd = tr.find_elements_by_css_selector('td.td-desc.more span:first-child')
            for desc in descTd:
                descr = desc.text
                break
            
            # 庫存數
            stockQy = tr.find_elements_by_css_selector('td.td-stock')
            for stock in stockQy:
                stockQty = stock.text
                break


            # 價格
            values = tr.find_elements_by_css_selector('td ul.price-list li')
            for value in values:
                try:
                    batch = value.find_element_by_css_selector('span.label')
                    price = value.find_element_by_css_selector('span.value')
                    new = pd.DataFrame.from_dict( {"itemFilter":[itemFilter],
                                                   "item":[itemLink],
                                                   "manu":[manu],
                                                   "descr":[descr],
                                                   "stockQty":[stockQty],
                                                   "firmName":[firmName.text],
                                                   "link":[href],
                                                   "quantity":[batch.text],
                                                   "price":[price.text] }) 
                    price_df = price_df.append(new,ignore_index=True)
                except:
                    print("------")
    driver.close()

f.close()



    
#df = pd.read_json (txtFileName)
#export_csv = df.to_csv (txtFileName+'.csv', index = None, header=True)
price_df.to_csv(fileName)
print("program end")
