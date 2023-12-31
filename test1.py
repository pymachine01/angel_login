from smartapi import SmartConnect
import pandas as pd
from datetime import datetime
import credentials
import requests
import numpy as np
import pyotp
import sleep

myotp =  pyotp.TOTP(credentials.CD).now()

def place_order(token,symbol,qty,exch_seg,buy_sell,ordertype,price):
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
            }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))

def intializeSymbolTokenMap():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    global token_df
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike': float})
    credentials.TOKEN_MAP = token_df
    print(token_df.index)
    input()

def getTokenInfo (exch_seg, instrumenttype,symbol,strike_price,pe_ce):
    df = credentials.TOKEN_MAP
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])


if __name__ == '__main__':
   # intializeSymbolTokenMap()
   # print(token_df)
    print(888888888888888888888888888888)
   # print(credentials.TOKEN_MAP)
input("-----------------------------------------")

obj=SmartConnect(api_key=credentials.API_KEY)
data = obj.generateSession(credentials.USER_NAME,credentials.PWD,myotp)
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
credentials.FEED_TOKEN = feedToken

userProfile= obj.getProfile(refreshToken)  

print(userProfile)
input("-----------------------------------------")
input("-----------------------------------------")
#Historic api
try:
    historicParam={
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-08 09:00", 
    "todate": "2021-02-08 09:16"
    }
    v=obj.getCandleData(historicParam)
    print(v)
except Exception as e:
    print("Historic Api failed: {}".format(e.message))
#logout
input("-----------------------------------------")

tokenInfo = getTokenInfo('NFO','OPTIDX','NIFTY',18900,'PE').iloc[0]
print(tokenInfo)
symbol  = tokenInfo['symbol']
token = tokenInfo['token']

input("-----------------------------------------")
input("-----------------------------------------")
input("-----------------------------------------")

lot = int(tokenInfo['lotsize'])
print(symbol, token, lot)

#place_order(token,symbol,lot,'NFO','BUY','MARKET',200)
