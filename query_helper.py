#!/usr/bin/env python
# coding: utf-8

# In[25]:


import config
import json
import requests
import vulture_scraper as vulture
api_key = config.API_key
import time 
import datetime
import mysql.connector
from mysql.connector import errorcode
import pandas as pd



# In[26]:


def connect():
    global cnx
    cnx = mysql.connector.connect(
    host = config.host,
    user = config.admin,
    passwd = config.password,
    database = 'Movies')
    global cursor
    cursor = cnx.cursor()


# In[9]:


def query(query_string):
    connect()
    cursor = cnx.cursor()
    
    cursor.execute(query_string)
    return cursor.fetchall()
    
    
def query_to_df(query_string):
    connect()
    cursor = cnx.cursor()
    
    cursor.execute(query_string)
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns = [x[0] for x in cursor.description]
    return df

# In[17]:


def create_table(create_query):    
    cursor = cnx.cursor()
    try:
        print("Creating a new table")
        cursor.execute(create_query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    cnx.close()


# In[51]:


def insert_imdb(movie_dict):
    list_of_tuples = [tuple(t.values()) for t in movie_dict]
    cursor = cnx.cursor()
    insert_statement = """INSERT IGNORE INTO imdb(
                   imdb_id,
                   cast,
                   key_words,
                   budget,
                   gross,
                   rating_value,
                   rating_count)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cursor.executemany(insert_statement, list_of_tuples)
    cnx.commit()

def db_insert(movie_dict):
    list_of_tuples = []
    for movie in movie_dict:
        temp_tuple = ()
        temp_tuple = (movie['id'],
              movie['title'],
              movie['budget'],
              movie['revenue'],
              movie['genres'],
              movie['original_language'],
              movie['overview'],
              movie['collection'],
              movie['popularity'],
              movie['production_company'],
              movie['production_countries'],
              movie['release_date'],
              movie['run_time'],
              movie['spoken_lang'],
              movie['tagline'],
              movie['vote_avg'],
              movie['vote_count'],
              movie['imdb_id'])
        list_of_tuples.append(temp_tuple)
    
    
## NOW we insert into out db
    #open connection
    cnx = mysql.connector.connect(
    host = config.host,
    user = config.admin,
    passwd = config.password,
    database = "Movies")
    
    #create cursor
    cursor = cnx.cursor()

    insert_statement = ("""INSERT IGNORE INTO tmdb_(
                      id,
                      title,
                      budget,
                      revenue,
                      genres,
                      original_language,
                      overview,
                      collection,
                      popularity,
                      production_companies,
                      production_country,
                      release_date,
                      run_time,
                      spoken_lang,
                      tagline,
                      vote_avg,
                      vote_count,
                      imdb_id)
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

    
    #empty dict to store id we've already inserted
    cursor.executemany(insert_statement, list_of_tuples)
    cnx.commit() 
    
    cursor.close()
    cnx.close()
    


# In[ ]:




