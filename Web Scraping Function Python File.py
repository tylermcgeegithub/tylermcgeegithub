#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Written by Tyler McGee, 2/18/2020
#Adapted from https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
import pandas as pd
import numpy as np
import requests
import lxml.html as lh
import matplotlib.pyplot as plt
import re

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


def cleanString(a):
    b = a.replace('\t','')
    c = b.replace('\r','')
    d = c.replace('\n','')
    return d


# In[ ]:


def webScrapeTable(url, xPathy, rowLength):
    ###url = "https://www.atptour.com/en/rankings/singles"
    ###!!!!!!!!!!!! Inspect the webpage and xpath should be like this '//*[@id="pageEventH2hTable"]/table/tbody/tr'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath(xPathy)
    ##
    ##
    ####Check the length of the first 12 rows
    ###[len(T) for T in tr_elements[:12]]
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        name = cleanString(name)
        #print('%d:"%s"' % (i,name))
        col.append((name,[]))
    ##
    ##
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        i = 0
        
        #If row is not of size rowLength, the //tr data is not from our table 
        if len(T)!=rowLength:
            if len(T) == rowLength-1:
                i = 1
                col[0][1].append(0)
            else:
                continue
                #break
    
        ##i is the index of our column
        #i=0
    
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            data = cleanString(data)
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
    ##
    ##
    #[len(C) for (title,C) in col] Use this to check that each column is the same length
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    df.head()
    return df


# In[ ]:


#Use this cell to check that everything compiles correctly and runs correctly
#Last checked 2/18/2020
url = "https://www.atptour.com/en/players/atp-head-2-head/alexander-zverev-vs-dominic-thiem/Z355/TB69"
pathy = '//*[@id="pageEventH2hTable"]/table/tbody/tr'
rowLen = 6
ThiemZverevFunctionCheck = webScrapeTable(url, pathy, rowLen)
ThiemZverevFunctionCheck.head()

