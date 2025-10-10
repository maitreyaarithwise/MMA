# MMA
Repository contains MMA files and folders

##### Platfrom Credentials
kalshi & prophetx login
email: atfcapital1@gmail.com
pw: Chang3MeNowASAP!

##### Work Flow
Pinnacle sends live odds for “Patriots vs Eagles”.
Maitreya (Admin) sets automation rule [Fixed In BE]:
If Pinnacle odds move 0.05 → update Kalshi quote.
Max quote = $500, exposure = $1500, stop-loss = $300/day.
System posts quote to Kalshi.
Bettor_001 takes Trader_001’s quote.
Match ends → Kalshi marks event “resolved”.
System updates Trader_001’s P&L using result.
Counterparty tracker marks Bettor_001 as “sharp”.
Next time, system reduces quote size for Bettor_001.

##### Example Events of Various Platforms
Pinnacle → "49ers @ Cowboys - Spread - Cowboys -3.5"
Kalshi → "Will Cowboys win by more than 3.5 points? Yes/No"
ProphetX → "NFL: DAL vs SF, Handicap 3.5"

##### Example JSON Formats of Various Platforms
{
  "event_id": "pin_3322",
  "league": "NFL",
  "teams": ["San Francisco 49ers", "Dallas Cowboys"],
  "market_type": "moneyline",
  "prices": {
    "49ers": +110,
    "Cowboys": -120
  }
}

{
  "event_id": "kal_8765",
  "event_name": "49ers vs Cowboys",
  "market_question": "Will Cowboys win?",
  "contracts": [
    {"contract_id": "YES", "price": 0.54},
    {"contract_id": "NO", "price": 0.46}
  ]
}

{
  "market_id": "px_9090",
  "sport": "NFL",
  "matchup": "DAL vs SF",
  "type": "winner",
  "odds": {
    "DAL": -118,
    "SF": +112
  }
}