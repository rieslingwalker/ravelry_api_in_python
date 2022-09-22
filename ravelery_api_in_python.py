#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# import packages needed
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import http.client
import json
import requests
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#test to make sure we can do API calls
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
r = requests.get('https://www.office.com')  # how to make the request 
print(r) # to see if we get a valid output code
print(r.iter_lines()) # what the output code means
# print(r.text) # what the output of the request is.  This is commented out becuase it is very long
r.close() # closes the request.  Best practice.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# trying out the ravelry API for the first time
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# load API token username and password
# Please input your own credentials which you can make at https://www.ravelry.com/groups/ravelry-api
authUsername = '<your credentials>'
authPassword = '<your credentials>'

#define URL for the API request
url = 'https://api.ravelry.com/color_families.json'      
#make the request
r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
#close the connection
r1.close()

print("response code: {}".format(r1)) #tells me the response code
print("response code Details: {}".format(r1.iter_lines())) #tells me details about the response code
print("response output:")
print(r1.text) #tells me the output
print("response output formatted:")
print(json.dumps(json.loads(r1.text), indent=4)) #makes the json more readable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# trying an API request with parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#define URL for the API request
url = 'https://api.ravelry.com/patterns/search.json'      
#make the request
r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
#close the connection
r1.close()

print("response code: {}".format(r1)) #tells me the response code
print("response code Details: {}".format(r1.iter_lines())) #tells me details about the response code
print("response output:")
print(r1.text) #tells me the output
print("response output formatted:")
print(json.dumps(json.loads(r1.text), indent=4)) #makes the json more readable


#define parameters
query = 'flamingo'
page = 6
page_size = 2
craft = 'knitting'

#define URL for the API request
url = 'https://api.ravelry.com/patterns/search.json?query={}&page={}&page_size={}&craft={}'.format(query, page, page_size, craft)      
#make the request
r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
#close the connection
r1.close()

print("response code: {}".format(r1)) #tells me the response code
print("response code Details: {}".format(r1.iter_lines())) #tells me details about the response code
print("response output:")
print(r1.text) #tells me the output
print("response output formatted:")
print(json.dumps(json.loads(r1.text), indent=4)) #makes the json more readable


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# defining a function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_patterns(authUsername, authPassword, query = '', page = 1, page_size = 100, craft = 'knitting') -> pd.core.frame.DataFrame:
    #define URL
    url = 'https://api.ravelry.com/patterns/search.json?query={}&page={}&page_size={}&craft={}'.format(query, page, page_size, craft)  
    #make the request
    r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(authUsername, authPassword))
    #close the connection
    r1.close()
  
    #I decided for this project we will not use the paginator part of the json, and it would be easier to output a dataframe from the function allowing for analysis right away
    return pd.DataFrame.from_records(json.loads(r1.text)['patterns'])
  
print( get_patterns(authUsername, authPassword, query = 'flamingo', page = 6, page_size = 2, craft = 'knitting')['name'] )
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# defining an unrelated class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class pet:
    def __init__(self, animal_type, owner, name):
        self.animal_type = animal_type
        self.owner = owner
        self.name = name

    def introduction(self):
        output = "Hi! I'm {}'s {} named {}.'".format(self.owner, self.animal_type, self.name)
        return output

hamilton = pet('cat', 'Katie', 'Hamilton')

print(hamilton.introduction())
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# defining ravelry api class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class raveleryutils:

    # first, set up everything that you will need to connect to the API.
    def __init__(self, authUsername:str, authPassword:str):
        self.authUsername = authUsername
        self.authPassword = authPassword
        
    
    #next, define any functions you will need.  This way, we define it once but can use it as many times as we would like
    
    # this returns all valid color families
    def get_color_families(self) -> pd.core.frame.DataFrame:
        #define URL
        url = 'https://api.ravelry.com/color_families.json'      
        #make the request
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        r1.close()
        
        return pd.DataFrame.from_records(json.loads(r1.text)['color_families'])
    
    # This returns the pattens from search.  Parameters include query (like "hats"), page number, page size, and craft
    def get_patterns(self, query = '', page = 1, page_size = 100, craft = 'knitting') -> pd.core.frame.DataFrame:
        #define URL
        url = 'https://api.ravelry.com/patterns/search.json?query={}&page={}&page_size={}&craft={}'.format(query, page, page_size, craft)  
        #make the request
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        r1.close()
        
        return pd.DataFrame.from_records(json.loads(r1.text)['patterns'])
    
    # This returns all the patterns from a given person's rav_username
    def get_queue(self, rav_username = 'rieslingm', query = '', page = 1, page_size = 100) -> pd.core.frame.DataFrame:
        #define URL
        url = 'https://api.ravelry.com/people/{}/queue/list.json?query={}&page={}&page_size={}'.format(rav_username, query, page, page_size) 
        #make the request
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        r1.close()
        
        return pd.DataFrame.from_records(json.loads(r1.text)['queued_projects'])
    
    
    # This returns all the favorites from a given person's rav_username
    # unfortuantely this has to be authenticated so this will not work :(
    def get_favorites(self, rav_username = 'rieslingm', types = 'patterns', query = '', deep_search = '', page = 1, page_size = 100) -> list:
        #define URL
        url = 'https://api.ravelry.com/people/{}/favorites/list.json?types={}&query={}&deep_search={}&page={}&page_size={}'.format(rav_username, types, query, deep_search, page, page_size) 
        #make the request
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        r1.close()
        
        print(r1.text)
        
        return json.loads(r1.text)[types]
      
#first, define an isntance of the class
raveleryutils_api = raveleryutils(authUsername, authPassword)

# Get yarn weights
color_families = raveleryutils_api.get_color_families()
display(color_families)

# TOP PATTERNS
top_hat_patterns = raveleryutils_api.get_patterns(query = 'hat', page = 15, page_size = 2) 
top_patterns = raveleryutils_api.get_patterns()
print("get_patterns columns: {}".format(top_patterns.columns))
print("top pattern names:" )
display(top_patterns['name'])

# QUEUED PATTERNS
#get the data
queued_patterns = raveleryutils_api.get_queue(rav_username = 'rieslingm', page_size = 1000)
print("queued_patterns columns: {}".format(queued_patterns.columns))
print("items in queue: {}".format(len(queued_patterns)))

# Favorites
# I know this will not work because my credentials are not good enough
favorite_patterns = raveleryutils_api.get_favorites(rav_username = 'rieslingm')
print("favorite_patterns columns: {}".format(favorite_patterns.columns))
