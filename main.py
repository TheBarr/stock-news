import requests
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("ALPHA_VANTAGE_KEY"),

}
date_now = dt.datetime.now().date()
date_yesterday = date_now - dt.timedelta(days=2)
date_day_before_yesterday = date_now - dt.timedelta(days=10)

response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()
stock_data_yesterday = float(response.json()['Time Series (Daily)'][str(date_yesterday)]['4. close'])
stock_data_day_before_yesterday = float(
    response.json()['Time Series (Daily)'][str(date_day_before_yesterday)]['4. close'])

percentage = round(100 - (stock_data_day_before_yesterday / stock_data_yesterday) * 100, 2)
if percentage >= 5 or percentage <= -5:
    print("Get News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
