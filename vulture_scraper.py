#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import json 


# In[78]:


def vulture_scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return list(set([x.text.strip('*') for x in soup.find_all('strong')]))


# In[84]:


netflix = "https://www.vulture.com/article/best-movies-on-netflix-right-now.html"
amazon = "https://www.vulture.com/article/best-movies-amazon-prime.html"
hulu = "https://www.vulture.com/article/best-movies-hulu-right-now.html"


# In[86]:


best_netflix = vulture_scrape(netflix)
best_amazon = vulture_scrape(amazon)
best_hulu = vulture_scrape(hulu)

