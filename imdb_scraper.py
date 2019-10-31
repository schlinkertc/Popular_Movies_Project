

import requests
from bs4 import BeautifulSoup
import json


## takes in a list of ids and returns rating data in a list of dictionaries

def find_rating(imdb_ids):
    ratings = []
    for imdb_id in imdb_ids:
        try:
            url = 'https://www.imdb.com/title/{}/'.format(imdb_id)

            r = requests.get(url)
            page = BeautifulSoup(r.content)
            post = page.find_all(attrs={'class':'ratingValue'})

            rating_value = float(post[0].find(itemprop="ratingValue").contents[0])
            num_user_ratings = float(list(post[0].find('strong').attrs.values())[0].split()[3].replace(',',''))

            rating = {}
            rating['imdb_id'] = imdb_id
            rating['value'] = rating_value
            rating['num_user_ratings'] = num_user_ratings

            ratings.append(rating)
        except: 
            None
    return ratings

## takes in a list of ids and returns [{id:id, cast:10 cast members}]

def get_credits(imdb_ids):
    credits = []
    for imdb_id in imdb_ids:
        url = 'https://www.imdb.com/title/{}/fullcredits/'.format(imdb_id)

        r = requests.get(url)
        page = BeautifulSoup(r.content)
        
        odd = page.find_all(attrs={'class':'odd'})
        even = page.find_all(attrs={'class':'even'})
        names = []
        for item in odd:
            names.append(item.find_all('a')[1].text.strip())
        for item in even:
            names.append(item.find_all('a')[1].text.strip())
            
        movie_credits = {}
        movie_credits['imdb_id'] = imdb_id
        movie_credits['cast'] = names[:10]
        
        credits.append(movie_credits)
    return credits

def get_keywords(imdb_ids):
    keywords = []
    for imdb_id in imdb_ids:
        url = 'https://www.imdb.com/title/{}/'.format(imdb_id)
        
        r = requests.get(url)
        page = BeautifulSoup(r.content)
        post = page.find_all(attrs={'class':'itemprop'})
        
        words = [x.getText() for x in post]
        
        keyword_dict = {}
        keyword_dict['id'] = imdb_id
        keyword_dict['keywords'] = words
        
        keywords.append(keyword_dict)
        
    return keywords

def get_box_office(imdb_ids):
    box_office = []
    for imdb_id in imdb_ids:
        try:
            url = 'https://www.imdb.com/title/{}/'.format(imdb_id)

            r = requests.get(url)
            page = BeautifulSoup(r.content)
            post = page.find_all(attrs={'class':['txt-block']})

            budget = int([x.getText().split()[0] for x in post][9:12:2][0].split('$')[1].replace(',',''))
            gross = int([x.getText().split() for x in post][9:12:2][1][-1].strip('$').replace(',',''))

            box_office_dict={}
            box_office_dict['id'] = imdb_id
            box_office_dict['budget'] = budget
            box_office_dict['gross'] = gross 

            box_office.append(box_office_dict)
        except:
            box_office_dict={}
            box_office_dict['id'] = None
            box_office_dict['budget'] = None
            box_office_dict['gross'] = None
    return box_office
