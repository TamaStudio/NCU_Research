import requests

query = 'Google LLC'

search_params = {
    'action': 'wbsearchentities',
    'format': 'json',
    'search': query,
    'language': 'en',
}

def fetch_wikidata(params):
    url = 'https://www.wikidata.org/w/api.php'
    try:
        return requests.get(url, params=params)
    except:
        return 'There was an error'

#Fetch API
data = fetch_wikidata(search_params)

#show response as JSON
data = data.json()

#print(data)

#Extracting the ID of the entity
entities_id = [] 
for elem in data['search']:
    entities_id.append(elem['id'])
    try:
        print (elem['description'])
    except:
        print('No description available')
