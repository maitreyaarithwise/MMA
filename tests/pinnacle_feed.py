'''DOCSTRING'''
import requests
import json
import pandas as pd

OUTPUT_FILE = "pinnacle_data.xlsx"

df = pd.DataFrame({
    "Name": ["Mitreya"],
    "Age": [23]
})

def save_to_excel(data, sheet_name):
    # Convert nested JSON to flat table
    df = pd.json_normalize(data)
    with pd.ExcelWriter(OUTPUT_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def get_pinnacle_periods():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/meta-periods"

    querystring = {"sport_id":"7"} # American Football

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    save_to_excel(data.get("periods", data), "Periods List")
    # print(json.dumps(response.json(), indent=4))

def get_pinnacle_sports():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/sports"

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    save_to_excel(data, "Sports List")
    # print(json.dumps(response.json(), indent=4))

def get_pinnacle_special_markets():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/special-markets"

    querystring = {"event_type":"prematch","sport_id":"7","is_have_odds":"true","league_ids":"889"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    save_to_excel(data.get("specials", data), "NFL Special Market List")
    # print(json.dumps(response.json(), indent=4))

def get_pinnacle_archieve_events():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/archive"

    querystring = {"sport_id":"7","page_num":"1","league_ids":"889"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    save_to_excel(data.get("events", data), "NFL Events List")
    # print(json.dumps(response.json(), indent=4))

def get_pinnacle_leagues():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/leagues"

    querystring = {"sport_id":"7"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    save_to_excel(data.get("leagues", data), "Leagues List")
    # print(json.dumps(response.json(), indent=4))    

def get_pinnacle_markets():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/markets"

    querystring = {"event_type":"prematch","sport_id":"7","is_have_odds":"true","league_ids":"889"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)  
    data = response.json()
    save_to_excel(data.get("events", data), "NFL Markets List")
    # print(json.dumps(response.json(), indent=4))

def get_pinnacle_event_details():
    '''DOCSTRING'''

    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/details"

    querystring = {"event_id":"1611816097"}

    headers = {
        "x-rapidapi-key": "4a1fe69c82mshc5dca8e31d75ad3p18b29djsn46f8caf03b8c",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    save_to_excel(data.get("events", data), "Specific Event Details")
    # print(json.dumps(response.json(), indent=4))

if __name__ == "__main__":
    # Create empty Excel before appending
    with pd.ExcelWriter(OUTPUT_FILE, mode="w", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="test", index=False)

    # Call all APIs
    # get_pinnacle_periods()
    # get_pinnacle_sports()
    # get_pinnacle_special_markets()
    # get_pinnacle_archieve_events()
    # get_pinnacle_leagues()
    # get_pinnacle_markets()
    # get_pinnacle_event_details()

    print(f"✅ All data saved to {OUTPUT_FILE}")
