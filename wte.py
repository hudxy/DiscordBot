import os
import requests, json
import random
from dotenv import load_dotenv
load_dotenv()

# enter your api key here
api_key = str(os.environ.get('GOOGLE_API'))
  
# url variable store url
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

static_string = 'food near '

def get_place(zip_code):
    # get method of requests module
    # return response object
    r = requests.get(url + 'query=' + static_string + zip_code + '&key=' + api_key)
    
    # json method of response object convert
    #  json format data into python format data
    x = r.json()
    # now x contains list of nested dictionaries
    # we know dictionary contain key value pair
    # store the value of result key in variable y
    y = x['results']
    z = random.choice(y)

    # Return name of random choice of results
    return z['name']
