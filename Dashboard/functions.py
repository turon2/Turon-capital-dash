import numpy as np
import pandas as pd
from calendar import monthrange
from datetime import date, timedelta, datetime

# try:
#     print("Trying to connect to the database")
#     # conn = pymysql.connect(host = '130.211.219.71',port=int(3306),user='root',passwd='Nodal@987',db='nodalDB')
#     # cur = conn.cursor()
# except:
#   print("Connection failed")

## Reading the data from the table
df = pd.read_csv("data/nifty_banknifty_stocks_list.csv",index_col=0)

def all():
    data = df.copy()
    data['trading_date'] = pd.to_datetime(data['trading_date'], format='%y%m%d', infer_datetime_format=True)
    data = data.astype(
        {"open": float, "high": float, "low": float, "close": float, "adj_close": float, "volume": float})

    return data
def monthly_data(stock : str, month = 1,year = 2015):
    num_days = monthrange(year, month)[1]
    data = df.copy()
    data = data[data['stock_name'] == stock]
    data['trading_date'] = pd.to_datetime(data['trading_date'], format='%y%m%d', infer_datetime_format=True)
    data = data[
        (data['trading_date'] >= datetime(year, month, 1)) & (data['trading_date'] <= datetime(year, month, num_days))]
    data = data.astype(
        {"open": float, "high": float, "low": float, "close": float, "adj_close": float, "volume": float})

    return data

def yearly_data(stock : str, year = 2015):
    data = df.copy()
    data = data[data['stock_name'] == stock]
    data['trading_date'] = pd.to_datetime(data['trading_date'], format='%y%m%d', infer_datetime_format=True)
    data = data[(data['trading_date'] >= datetime(year, 1, 1)) & (data['trading_date'] < datetime(year + 1, 1, 1))]
    data = data.astype(
        {"open": float, "high": float, "low": float, "close": float, "adj_close": float, "volume": float})

    return data

def all_time_data(stock : str):
    data = df.copy()
    data = data[data['stock_name'] == stock]
    data['trading_date'] = pd.to_datetime(data['trading_date'], format='%y%m%d', infer_datetime_format=True)
    data = data.astype(
        {"open": float, "high": float, "low": float, "close": float, "adj_close": float, "volume": float})

    return data

def log_returns(data_df):
    data = data_df.copy()
    log_returns = np.log(data.close / data.close.shift(1)).dropna()
    log_returns.index = data['trading_date'].to_numpy()[1:]
    returns = 100 * data.close.pct_change().dropna()
    returns.index = data['trading_date'].to_numpy()[1:]
    return returns

def trend(x):
    if x > -0.5 and x <= 0.5:
        return 'Slight or No change'
    elif x > 0.5 and x <= 1:
        return 'Slight Positive'
    elif x > -1 and x <= -0.5:
        return 'Slight Negative'
    elif x > 1 and x <= 3:
        return 'Positive'
    elif x > -3 and x <= -1:
        return 'Negative'
    elif x > 3 and x <= 7:
        return 'Among top gainers'
    elif x > -7 and x <= -3:
        return 'Among top losers'
    elif x > 7:
        return 'Bull run'
    elif x <= -7:
        return 'Bear drop'

def returns(data_df):
    data = data_df.copy()
    data["Day_Perc_Change"] = data['close'].pct_change() * 100
    data.dropna(axis=0, inplace=True)
    data['Trend'] = np.zeros(data['Day_Perc_Change'].count())
    data['Trend'] = data['Day_Perc_Change'].apply(lambda x: trend(x))
    pie_data = data.groupby('Trend')
    pie_label = sorted([i for i in data.loc[:, 'Trend'].unique()])

    return pie_data, pie_label

def screen():
    df = pd.read_csv("data/screener.csv", index_col=0)
    return df
if __name__ == '__main__':
    all()