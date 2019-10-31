import config
import json
import requests
import vulture_scraper as vulture
api_key = config.API_key
import time
import datetime 


## search a list of terms on MovieDB and return the results in a list of dictionaries 
def search_movies_timed(api_key, list_of_movies):
        lengthToSleep = 40/59
        
        data = []
        
        for movie in list_of_movies:
            url = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}".format(api_key,movie)
            data.append(requests.get(url).json())
            time.sleep(lengthToSleep)
            
        results_list_nested = [x.get('results') for x in data]
        results = [val for sublist in results_list_nested if type(sublist) == list for val in sublist] #<-- if clause makes sure that we're not iterating over none
        
        num_results = sum(filter(None,[x.get('total_results') for x in data])) # <--- not super useful but i was proud of the code
        
        return results 
    
# takes in a list of MovieDB_ids and returns the full MovieDB information on those movies 
def get_movies_timed(api_key,ids):
    
    lengthToSleep = 40/59        
    
    data = []
    for i in ids:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(i,api_key)
        data.append(requests.get(url).json())
        
        time.sleep(lengthToSleep)
        
    return data


## takes in a list of strings, and performs search and get functions simultaneously 
def search_and_get(api_key,list_of_movies):
    search = search_movies_timed(api_key,list_of_movies)
    
    ids = [d['id'] for d in search]
    
    return get_movies_timed(api_key,ids)

## key test for reference while creating tables

def key_test(list_of_dicts):
    return [{key:type(d.get(key)) for key in d.keys()} for d in list_of_dicts] 


#############Below are generic functions to query MovieDB################

## returns data from Movie DB's list of popular movies. updated daily 
def get_popular(api_key):

    url = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US".format(api_key)
    return requests.get(url).json()

## returns only the titles from Movie DB's list of popular movies 
def get_popular_titles(api_key):
    data = get_popular(api_key)
    return [x['title'] for x in data['results']]

## returns data from Movie DB's list of top rated movies 
def get_top_rated(api_key):
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=en-US".format(api_key)
    return requests.get(url).json()

## returns list of IDs from Movie DB's top rated movies 
def get_top_rated_ids(api_key):
    data = get_top_rated(api_key)
    return [x['id'] for x in data['results']]

# our original search function
## returns movie data when given an API key and list of movie titles 
def search_movies(api_key, list_of_movies):
    data = []
    for movie in list_of_movies[0:40]:
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}".format(api_key,movie)
        data.extend(requests.get(url).json()['results'])
        time.sleep(1)
    #time.sleep(10)
    for movie in list_of_movies[40:]:
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}".format(api_key,movie)
        data.extend(requests.get(url).json()['results'])
        time.sleep(1)
    return data

## returns full details when given a list of movie IDs
## our original get_movies function
def get_movies(api_key,ids):
    data = []
    for i in ids:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(i,api_key)
        time.sleep(.5)
        data.append(requests.get(url).json())
    return data