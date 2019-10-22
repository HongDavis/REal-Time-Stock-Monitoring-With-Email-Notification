# I have some stocks I want to sell and I want to sell at a price I think reasonable. Hence, I wrote this to email me when the market price of the stock exceeded my threshold or pre-determined price.

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time 

# This function is to send an email to notify the user when the price of the stock exceeded the threshold.
def sendemail():
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    pw = 'xxxx' # put in your email password.
    msg = MIMEMultipart()
    msg['From'] = 'youremailaddress2@gmail.com' # put in the send from email address.
    msg['To'] = 'recipient@yahoo.com' # Recipient's email address
    msg['Subject'] = 'BK Stock Price Breached Threshold'
    body = 'Threshold set at 45 and closing price is ' + str(close_data[-1])
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP("smtp.gmail.com", 587) # Find out from your email service provider their SMTP server details if you are using a different SMTP server.
    server.starttls() # Encrypt email using tls
    server.login(msg['From'], pw) # Login to your email account
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit() # Close the SMTP server
    print('Email sent to your yahoo email.')

# Due to confidentiality, the API key used in these codes is fake.
# # API key can be easily obtained from https://www.alphavantage.co/support/#api-key
api_key = 'xxxxxxxxxxxxxxxx' # Put in your alpha vantage api key. 

# Assign time series to variable 'ts'. Setting output format as pandas format.
ts = TimeSeries(key=api_key, output_format = "pandas")

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
close_data = data['4. close'] # this is to pull all the info from the closing data.
if close_data[-1] > 45:
    sendemail()
else:
    print('Email not sent as closing price is below threshold of $45. Current stock price is ' + str(close_data[-1]))
# Next, compute the % change in between each min
### percentage_change = close_data.pct_change()
### print(percentage_change)
# Only the last percentage change is of interest.
### last_change = percentage_change[-1]

# You can easily implement the in a while loop to monitor the stock price.