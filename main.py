import requests
from datetime import datetime
import os
from twilio.rest import Client

# Stock info
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API Keys
alphavantage = ""
newsapi = ""

# Twilio Info
account_sid = ""
auth_token = ""
twilio_number = ""
my_number = ""

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# TODO: Get the stock data using alphavantage api - DONE
ALPHAVANTAGE_endpoint = "https://www.alphavantage.co/query?"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alphavantage,
}
response1 = requests.get(ALPHAVANTAGE_endpoint, params=parameters)
response1.raise_for_status()

data = response1.json()['Time Series (Daily)']
# TODO: Find percent increase/decrease between yesterday and previous day - DONE
# Get closing price for yesterday
# Get the closing price for precious_day
# Difference = yesterday - previous_day
# Percentage = 100 * (difference / closing previous day)

# ==============================================================================================
# Time functions - Attempt 1
# Issues:
# - no data for days the stock market isn't open (Sat/Sun)
# today = datetime.now().today()  # Monday-Sunday --> 0-6
# yesterday = today - timedelta(1)
# previous_day = yesterday - timedelta(1)
#
# Update date format
today = datetime.today().strftime("%Y-%m-%d")
# yesterday = yesterday.strftime("%Y-%m-%d")
# previous_day = previous_day.strftime("%Y-%m-%d")

# Days
days_list = [k for k in data.keys()]
days_list = days_list[:2]
yesterday = days_list[0]
previous_day = days_list[1]

# Closing prices
price_list = [float(v['4. close']) for (k, v) in data.items()]  # Gets the closing prices
price_list = price_list[:2]  # Gets 'yesterday' and 'previous day'

closing_yesterday = price_list[0]
closing_previous = price_list[1]
difference = round(closing_yesterday - closing_previous, 2)
percentage = round(100 * (difference / closing_yesterday))

# TODO: Print("Get News") if 5% inc/dec - DONE
if percentage >= 5 or percentage <= -5:
    icon = "🤩" if percentage > 0 else "🔻"

# ==============================================================================================
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    # TODO: Get first 3 articles for company
    NEWS_endpoint = "https://newsapi.org/v2/everything?"
    news_parameters = {
        "apiKey": newsapi,
        "q": f'+{COMPANY_NAME}',
        "from": previous_day,
        "to": today,
        "language": "en",
        "sortBy": "recent",
        "pageSize": 3,
    }
    response2 = requests.get(NEWS_endpoint, params=news_parameters)
    response2.raise_for_status()
    news_data = response2.json()['articles']

    title = []
    description = []

    for article in news_data:
        title.append(article['title'])
        description.append(article['description'])

    article_data = {title[i]: description[i] for i in range(len(title))}

# ==============================================================================================

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.


    ## Optional: Format the SMS message like this:
    """TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
    gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
    show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
    or 
    "TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey 
    have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
    filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
    market crash. """

    """[STOCK NAME]: [PERCENTAGE] Headline: [TITLE]. Brief: [DESCRIPTION)"""
    # Would look something like this
    # {STOCK}: {icon}{percentage}% Headline: {TITLE}. Brief: {DESCRIPTION}

    client = Client(account_sid, auth_token)

    for k, v in article_data.items():
        message = client.messages \
                        .create(
                             body=f"{STOCK}: {icon}{percentage}% Headline: {k}. Brief: {v}",
                             from_=twilio_number,
                             to=my_number
                         )

        print(message.status)
