

import requests
from bs4 import BeautifulSoup
import json


## takes in a list of ids and returns data in a list of dictionaries

def get_all(imdb_ids):    
    imdb_table = []
    for imdb_id in imdb_ids:
        movie_dict = {}
        movie_dict['imdb_id'] = imdb_id
        #connect to the main page for the movie 
        
        cast_url = 'https://www.imdb.com/title/{}/fullcredits/'.format(imdb_id)
        url = 'https://www.imdb.com/title/{}/'.format(imdb_id)
        r = requests.get(url)
        page = BeautifulSoup(r.content)
        
        
        #get the cast members
        odd = page.find_all(attrs={'class':'odd'})
        even = page.find_all(attrs={'class':'even'})
        names = []
        
        try:
            for item in odd:
                names.append(item.find_all('a')[1].text.strip())
            for item in even:
                names.append(item.find_all('a')[1].text.strip())
            
            movie_dict['cast'] = ', '.join(names[:10])
        
        except:
            movie_dict['cast'] = None
        
        #get the keywords
        
        words_post = page.find_all(attrs={'class':'itemprop'})

        words = [x.getText() for x in words_post]
        movie_dict['keywords'] = ', '.join(words)

        #get box office info
        
        try:
            box_office_post = page.find_all(attrs={'class':['txt-block']})

            budget = int([x.getText().split()[0] for x in box_office_post][9:12:2][0].split('$')[1].replace(',',''))
            gross = int([x.getText().split() for x in box_office_post][9:12:2][1][-1].strip('$').replace(',',''))

            movie_dict['budget'] = budget
            movie_dict['gross'] = gross 

        except:
            movie_dict['budget'] = None
            movie_dict['gross'] = None
        
        #get rating info 
        
        try:

            ratings_post = page.find_all(attrs={'class':'ratingValue'})

            rating_value = float(ratings_post[0].find(itemprop="ratingValue").contents[0])
            num_user_ratings = float(list(ratings_post[0].find('strong').attrs.values())[0].split()[3].replace(',',''))

            movie_dict['rating_value'] = rating_value
            movie_dict['rating_count'] = num_user_ratings

        except: 
            movie_dict['rating_value'] = None
            movie_dict['rating_count'] = None

        imdb_table.append(movie_dict)
    return imdb_table
