import requests
import os
import datetime as dt
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("ALPHA_VANTAGE_KEY"),

}

date_now = dt.datetime.now().date()
date_yesterday = date_now - dt.timedelta(days=1)
date_day_before_yesterday = date_now - dt.timedelta(days=2)

stock_response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data_yesterday = float(stock_response.json()['Time Series (Daily)'][str(date_yesterday)]['4. close'])
stock_data_day_before_yesterday = float(
    stock_response.json()['Time Series (Daily)'][str(date_day_before_yesterday)]['4. close'])

percentage = round(100 - (stock_data_day_before_yesterday / stock_data_yesterday) * 100, 2)

if percentage >= 5 or percentage <= -5:
    news_parameters = {
        "apiKey": os.getenv("NEWS_KEY"),
        "q": COMPANY_NAME,
        "searchIn": "title,description",
        "from": date_day_before_yesterday,
        "to": date_yesterday,
        "sortBy": "relevancy",
        "pageSize": 3,
    }

    news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()

    if percentage >= 5:
        title = f"{COMPANY_NAME} Stock And News - {STOCK} 🔺{percentage}%"
    elif percentage <= -5:
        title = f"{COMPANY_NAME} Stock And News - {STOCK} 🔻{percentage}%"

    sender = os.getenv("FROM_EMAIL")
    receivers = os.getenv("TO_EMAIL")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = receivers

    articles = """<html><head></head><body>"""
    for i in range(3):
        articles += "<b>" + news_response.json()["articles"][i]["title"] + "</b>" + "<br>"
        articles += news_response.json()["articles"][i]["description"] + "<br>" + "<br>"
    articles += """</body> </html>"""
    text = MIMEText(articles, "html")
    msg.attach(text)

    with smtplib.SMTP("smtp.gmail.com") as conn:
        conn.starttls()
        conn.login(user=sender, password=os.getenv("FROM_EMAIL_PASSWORD"))
        conn.sendmail(sender, receivers, msg.as_string())
        print("Email sent")