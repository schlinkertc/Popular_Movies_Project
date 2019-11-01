import config
import json
import requests
import vulture_scraper as vulture
api_key = config.API_key
import time
import datetime 
import query_helper

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
query_helper.connect()
def search_and_get(api_key,list_of_movies):
    search = search_movies_timed(api_key,list_of_movies)
    
    exists = query_helper.query("""select imdb_id from Movies.tmdb_;""")
    exists = [x[0] for x in exists]
    
    ids = [d['id'] for d in search if d['id'] not in exists]
    
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

def parse_function(search_results):
    results = []
    for d in search_results:
        if (d['imdb_id'] != '' and d['imdb_id'] != None and d['status'] == 'Released'):
            parsed_results = {}

            parsed_results['id'] = d.get('id')
            parsed_results['original_language'] = d['original_language']
            parsed_results['overview'] = d.get('overview')
            parsed_results['title'] = d.get('title')
            parsed_results['popularity'] = d.get('popularity')

            if d['belongs_to_collection'] == None:
                parsed_results['collection'] = None
            else: 
                parsed_results['collection'] = d['belongs_to_collection']['name']
                #make list into str
                temp = ''
                for i in parsed_results['collection']:
                    temp += i + ' '
                parsed_results['collection'] = temp

            parsed_results['budget'] = d.get('budget')
            parsed_results['revenue'] = d.get('revenue')

            if len(d['genres']) == 0:
                parsed_results['genres'] = None
            else:
                parsed_results['genres'] = [x['name'] for x in d['genres']]
                                #make list into str
                temp = ''
                for i in parsed_results['genres']:
                    temp += i + ' '
                parsed_results['genres'] = temp


            if len(d['production_companies']) == 0:
                parsed_results['production_company'] = None
            else:
                parsed_results['production_company'] = [x['name'] for x in d['production_companies']]
                                                #make list into str
                temp = ''
                for i in parsed_results['production_company']:
                    temp += i + ' '
                parsed_results['production_company'] = temp

            if len(d['production_countries']) == 0:
                parsed_results['production_countries'] = None
            else:
                parsed_results['production_countries'] = [x['name'] for x in d['production_countries']]
                                                #make list into str
                temp = ''
                for i in parsed_results['production_countries']:
                    temp += i + ' '
                parsed_results['production_countries'] = temp

            if d['release_date'] == '':
                parsed_results['release_date'] = None 
            else:
                parsed_results['release_date'] = datetime.datetime.strptime(d['release_date'],"%Y-%m-%d").date()

            if d['runtime'] == None:
                parsed_results['run_time'] = None
            else:
                parsed_results['run_time'] = d['runtime']
           
            if len(d['spoken_languages']) == 0:
                parsed_results['spoken_lang'] = None 
            else:
                parsed_results['spoken_lang'] = [x['name'] for x in d['spoken_languages']]
                                                #make list into str
                temp = ''
                for i in parsed_results['spoken_lang']:
                    temp += i + ' '
                parsed_results['spoken_lang'] = temp
            
            if d['tagline'] == '':
                parsed_results['tagline'] = None
            else: 
                parsed_results['tagline'] = d['tagline']
            
            parsed_results['vote_avg'] = d['vote_average']
            parsed_results['vote_count'] = d['vote_count']
            parsed_results['imdb_id'] = d['imdb_id']
            parsed_results['vote_count'] = d['vote_count']
            
            
            results.append(parsed_results)
    return results