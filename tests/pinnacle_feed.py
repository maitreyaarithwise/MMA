'''DOCSTRING'''
import requests
import json

def get_pinnacle_periods():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/meta-periods"

    querystring = {"sport_id":"7"} # American Football

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))

def get_pinnacle_sports():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/sports"

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(json.dumps(response.json(), indent=4))

def get_pinnacle_special_markets():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/special-markets"

    querystring = {"event_type":"prematch","sport_id":"7","is_have_odds":"true"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))

def get_pinnacle_archieve_events():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/archive"

    querystring = {"sport_id":"1","page_num":"1"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))

def get_pinnacle_leagues():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/leagues"

    querystring = {"sport_id":"7"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))    

def get_pinnacle_markets():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/markets"

    querystring = {"event_type":"prematch","sport_id":"7","is_have_odds":"true"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)  

    print(json.dumps(response.json(), indent=4))

def get_pinnacle_event_details():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/details"

    querystring = {"event_id":"1611584439"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(json.dumps(response.json(), indent=4))

# get_pinnacle_periods()
# get_pinnacle_sports()
# get_pinnacle_special_markets()
# get_pinnacle_archieve_events()
# get_pinnacle_leagues()
# get_pinnacle_markets()
# get_pinnacle_event_details()
