#!/usr/bin/env python
# coding: utf-8

# In[91]:


import requests
from bs4 import BeautifulSoup
import json


# In[105]:


movieDB_id = ['tt0355032']
url = 'https://www.imdb.com/title/{}/'.format(movieDB_id)


# In[41]:



r = requests.get(url)
page = BeautifulSoup(r.content)


# In[106]:


## takes in a list of movieDB_ids and returns imdb rating
#

def find_review(movieDB_ids):
    for movieDB_id in movieDB_ids:
        url = 'https://www.imdb.com/title/{}/'.format(movieDB_id)
        
        r = requests.get(url)
        page = BeautifulSoup(r.content)
        post = page.find_all(attrs={'class':'ratingValue'})
        
        return post[0].find(itemprop="ratingValue").contents


# In[107]:


find_review(movieDB_id)


# In[ ]:




