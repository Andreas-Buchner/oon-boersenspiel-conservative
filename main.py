import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import yfinance as yf
import re


def main():
    df = pd.read_csv("symbols.csv")

    df['Volatility'] = df.apply(lambda row: get_vola_3y(row.Symbol), axis=1)
    df.dropna(inplace=True)
    df.sort_values(by='Volatility', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df[:int(len(df) / 2) + 1]

    df['Momentum'] = df.apply(lambda row: get_mom_1y(row.Symbol), axis=1)
    df.dropna(inplace=True)
    df.sort_values(by='Momentum', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Mom Ranking'] = df.index + 1

    df['Total Yield'] = df.apply(lambda row: get_total_yield(row.Symbol), axis=1)
    df.dropna(inplace=True)
    df.sort_values(by='Total Yield', inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df['TY Ranking'] = df.index + 1

    df['Rating'] = (df['Mom Ranking'] + df['TY Ranking']) / 2
    df.sort_values(by='Rating', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Ranking'] = df.index + 1

    print(df)
    df.to_csv("rating.csv", index=False)


def get_mom_1y(symbol):
    print("Calculate 1y Momentum of {}".format(symbol))
    df = yf.Ticker(symbol).history(period="1y", interval="1d", actions=False)
    if len(df) < 252:
        print("Error {}: {} not in the market long enough".format(time.time(), symbol))
        return np.NAN
    df.drop(['Open', 'High', 'Low', 'Volume'], inplace=True, axis=1)
    return np.divide(df['Close'].iloc[-1], df['Close'].iloc[0])


def get_vola_3y(symbol):
    print("Calculate 3y Volatility of {}".format(symbol))
    df = yf.Ticker(symbol).history(period="5y", interval="1d", actions=False)
    if len(df) < 757:
        print("Error {}: {} not in the market long enough".format(time.time(), symbol))
        return np.NAN
    df.drop(['Open', 'High', 'Low', 'Volume'], inplace=True, axis=1)
    df = df[-757:]
    df['ROC'] = df.pct_change(1)
    df = df[1:]
    return df['ROC'].std()


def get_total_yield(symbol):
    """
    :param symbol: The Symbol of the Stock as a String
    :return: The Buyback Yield as a Float in % (e.g. 3.2 means 3.2%)
    """
    print("Fetching Total Yield for {}".format(symbol))
    while True:
        resp = requests.get("https://www.gurufocus.com/term/TotalPayoutYield/" + symbol + "/")
        if resp.status_code == 200:
            break
        print("Error, got Status Code " + str(resp.status_code))
        time.sleep(10)
    soup = BeautifulSoup(resp.content, 'html.parser')
    result = soup.findAll("strong")
    for r in result:
        if '%' in r.next:
            return float(r.next[:-1])
    return np.NAN  # no matching data found --> GuruFocus does not know this symbol


if __name__ == '__main__':
    main()
