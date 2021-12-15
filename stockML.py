# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 15:35:07 2021

@author: Odin
"""
# Machine learning dependanices
import pandas as pd
import quandl
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics

from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LinearRegression

import datetime
import time
import sys


def VEDAML(StockName, short_window, long_window, StartDate, EndDate):

    df = quandl.get(StockName, start_date=StartDate, end_date=EndDate)
    forecast_out = int(math.ceil(0.01*len(df)))
    forecast_out = 1
    # forecast_out = 180
    forecast_col = 'Value'
    df['label'] = df[forecast_col].shift(-forecast_out)
    # df.fillna(-9999, inplace=True)
    # Create buy/sell logic
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0

    # SMA Short window
    signals['short_mavg'] = df[forecast_col].rolling(window=short_window, min_periods = 1, center=False).mean()
    # SMA Long Window
    signals['long_mavg'] = df[forecast_col].rolling(window=long_window, min_periods = 1, center=False).mean()
    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                    > signals['long_mavg'][short_window:], 1.0,0.0)

    # Trading orders n ting
    signals['positions'] = signals['signal'].diff()

    SMAbuilder = "SMA"
    LMAbuilder = "LMA"
    df[SMAbuilder] = signals['short_mavg']
    df[LMAbuilder] = signals['long_mavg']

    capital = 10000
    # Positions dataframe
    positions = pd.DataFrame(index=signals.index).fillna(0)

    # 1000 shares = £29.45GBP
    positions['Position in EUR/USD'] = 1000*abs(signals['signal'])

    # initialise
    portfolio = positions.multiply(df[forecast_col], axis=0)

    # difference
    pos_diff = positions.diff()

    # Holdings
    #portfolio['holdings'] = (positions.multiply(df[forecast_col], axis=0)).sum(axis=1)
    portfolio['holdings'] = (positions.multiply(df[forecast_col]*1.12, axis=0)).sum(axis=1)

    # Cash
    portfolio['cash'] = capital - (pos_diff.multiply(df[forecast_col], axis = 0)).sum(axis=1).cumsum()

    # Total
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']

    # Returns
    portfolio['returns'] = portfolio['total'].pct_change()
    # cleanup
    del portfolio['Position in EUR/USD']

    # ML model
    X = np.array(df.drop(["label"], 1))
    X.autocorr()
    print(X)
    X = preprocessing.scale(X)
    X = X[:-forecast_out]
    X_lately = X[-forecast_out:]

    df.dropna(inplace=True)

    y = np.array(df['label'])

    # Training and test classifier
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size = 0.2)

    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    # prediction
    forecast_set = clf.predict(X_lately)
    print('Total: ', max(portfolio['total']))
    print("Predicted prices in the next ",
          forecast_out,
          " Days",
          forecast_set,
          "\nModel Accuracy : ", accuracy)

    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    df['Forecast'] = np.nan

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        print(next_date)
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

    graph = df.plot()
    # Buy
    graph.plot(signals.loc[signals.positions == 1.0].index,
               signals.short_mavg[signals.positions == 1.0],
               '^', markersize=20, color='g')
    # Sell
    graph.plot(signals.loc[signals.positions == -1.0].index,
               signals.short_mavg[signals.positions == -1.0],
               '^', markersize=20, color='r')
    graph.set_ylabel('Price')
    graph.set_title('EUR/USD', fontsize=20)
    # self.ids.accuracy.text = str("{:.2f}".format(accuracy))
    plt.savefig('GraphKun.png')
    plt.savefig('GraphKun1.png')
    plt.clf()

    forecast_data = ""
    # build string for predicted prices
    for x in forecast_set:
        forecast_data = forecast_data + " \n" + str(x)
    package = [accuracy, statistics.mean(forecast_set), max(portfolio['total'])]
    return package
