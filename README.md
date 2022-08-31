# Stock Checker
Program designed to check when there is a 5% change in a specific stock. Once a change is detected, a SMS message containing the percent change and news articles on the stock company will be sent to a specified phone number. 
This is done through the use of three APIs:
1. Alpha Vantage API - uses GET request to obtain current stock price
2. News API - uses GET request to retrieve current news articles
3. Twilio API - uses REST API to send SMS message
