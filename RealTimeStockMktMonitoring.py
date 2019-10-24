# This Python script is about selling some of my stock when the market price meets my expectation. When the condition is met, a notification will be sent to me via email.
# First, setup an account with Alpha Vantage so that I can download stock price via an API call.
# Assumption: Python3 and the necessary library eg, pandas are already installed. 

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import os # Required to access system environment variables eg, email address, password

# This function sends an email to notify the user when the stock price meets the threshold.
def sendemail(stpxthreshold,stpxcurrent):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    pw = os.environ.get('MailPW') # Email password
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('FromMailID') # Sender's email address.
    msg['To'] = os.environ.get('ToMailID') # Recipient's email address
    msg['Subject'] = 'BK Stock Price Breached Selling Price Threshold'
    body = 'Threshold set at ' + str(stpxthreshold) + '; current closing price is $' + str(stpxcurrent)
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP("smtp.gmail.com", 587) # Find out SMTP details from email service provider.
    server.starttls() # Encrypt email using tls
    server.login(msg['From'], pw) # Login to email account
    server.sendmail(msg['From'], msg['To'], msg.as_string()) # Send email
    server.quit() # Close the SMTP server
    print('Email sent to your yahoo email.')

# API key can be easily obtained from https://www.alphavantage.co/support/#api-key
api_key = os.environ.get('AlphaVantageAPI') # Put in your alpha vantage api key. 

# Assign time series to variable 'ts'. Setting output format as pandas format.
ts = TimeSeries(key = api_key, output_format = "pandas")

# Next, get stock data from the web and assign the data to variables
# data and meta_data. 
data, meta_data = ts.get_intraday(symbol= "BK", interval = '1min', outputsize = 'full')
### print(data) # Uncomment this to check whether data is pulled successfully.

# To save the data in an Excel file contineously, use a while loop;
### i = 1
# Uncomment the below codes to save data to an Excel file.
### while i ==1:
###     data, meta_data = ts.get_intraday(symbol= "BK", interval = '1min', outputsize = 'full')
    # Since the interval was set at 1 min above ie, to get the stock data on 1 min interval likewise, save the file in 1 min interval.
###     time.sleep(60)  # 60 seconds = 1 min

# To pull real time data down to the minute, this tentamount to day trading. Day trading is making all the money using the the volatility of the stock. Top find the volatility of the stock in a given min,# first thing needed is the closing data in each min.
stpxthreshold = 45.00 # Threshold stock price
close_data = data['4. close'] # this is to pull all the info from the closing data.
if close_data[-1] > stpxthreshold:
    sendemail(stpxthreshold, close_data[-1])
else:
    print('Email not sent as closing price is below threshold of ' + str(stpxthreshold) + '. Current stock price is ' + str(close_data[-1]))
# Compute the % change in between each min
### percentage_change = close_data.pct_change()
### print(percentage_change)
# Only the last percentage change is of interest.
### last_change = percentage_change[-1]
