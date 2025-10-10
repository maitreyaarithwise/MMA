import requests
import json
import pandas as pd

OUTPUT_FILE = "kalshi_data.xlsx"

df = pd.DataFrame({
    "Name": ["Mitreya"],
    "Age": [23]
})

def save_to_excel(data, sheet_name):
    # Convert nested JSON to flat table
    df = pd.json_normalize(data)
    with pd.ExcelWriter(OUTPUT_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def get_all_events():
    URL = "https://api.elections.kalshi.com/trade-api/v2/events"
    params = {"limit": 100}
    response = requests.get(URL, params=params)
    data = response.json()
    save_to_excel(data.get("events", data), "All_Events")

def get_event():
    event_ticker = 'KXELONMARS-99'
    URL = f"https://api.elections.kalshi.com/trade-api/v2/events/{event_ticker}"
    response = requests.get(URL)
    data = response.json()
    save_to_excel(data, "Event")

def get_markets():
    URL = "https://api.elections.kalshi.com/trade-api/v2/markets"
    params = {"limit": 100}
    response = requests.get(URL, params=params)
    data = response.json()
    save_to_excel(data.get("markets", data), "Markets")

def get_market():
    ticker = 'KXHIGHCHI-25SEP18-T87'
    URL = f"https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"
    response = requests.get(URL)
    data = response.json()
    save_to_excel(data, "Market")

def get_trades():
    URL = "https://api.elections.kalshi.com/trade-api/v2/markets/trades"
    params = {"limit": 100}
    response = requests.get(URL, params=params)
    data = response.json()
    save_to_excel(data.get("trades", data), "Trades")

def get_series_list():
    URL = "https://api.elections.kalshi.com/trade-api/v2/series"
    params = {"limit": 100, "category": "Sports"}
    response = requests.get(URL, params=params)
    data = response.json()
    save_to_excel(data.get("series", data), "Series_List")

def get_series():
    series_ticker = 'KXLCKAHRIPICK'
    URL = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}"
    response = requests.get(URL)
    data = response.json()
    save_to_excel(data, "Series")

def get_milestones():
    URL = f"https://api.elections.kalshi.com/trade-api/v2/milestones"
    params = {"limit": 100}
    response = requests.get(URL, params=params)
    data = response.json()
    save_to_excel(data, "Milestones")

# def get_forecast_history():
#     ticker = 'KXNBASEATTLE-30'
#     URL = f"https://api.elections.kalshi.com/trade-api/v2/cached/events/{ticker}/forecast_history"
#     response = requests.get(URL)
#     try:
#         data = response.json()
#         save_to_excel(data, "Event Forcast History")
#     except json.JSONDecodeError as e:
#         print("⚠️ JSON decode error:", e)
#         print("Status Code:", response.status_code)
#         print("Content-Type:", response.headers.get("Content-Type"))
#         print("Raw Response (first 500 chars):")
#         print(response.text[:500])   # show first 500 characters
#         return None

# def get_event_candlesticks():
#     ticker = 'KXNBASEATTLE-30'
#     URL = f"https://api.elections.kalshi.com/trade-api/v2/events/{ticker}/candlesticks"
#     response = requests.get(URL)
#     data = response.json()
#     save_to_excel(data, "Event Candlesticks")

if __name__ == "__main__":
    # Create empty Excel before appending
    with pd.ExcelWriter(OUTPUT_FILE, mode="w", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="test", index=False)

    # Call all APIs
    get_all_events()
    get_event()
    get_markets()
    get_market()
    get_trades()
    get_series_list()
    get_series()
    get_milestones()
    # get_forecast_history()
    # get_event_candlesticks()

    print(f"✅ All data saved to {OUTPUT_FILE}")
