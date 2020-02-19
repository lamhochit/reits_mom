import pandas as pd
import numpy as np
import pathlib
import os


def data_lister():
    list_stock = []
    directory = pathlib.Path.cwd() / 'REITS_Data'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith("fundamental.csv"):
                list_stock.append(file)

    return list_stock


def data_reader(reits_code):
    reits_code = reits_code
    df = pd.read_csv(pathlib.Path.cwd() / 'REITS_Data' / reits_code)
    return df


def momentum_roc(df, period='5D'):
    freq = {'5D': 5,
            '1M': 21,
            '3M': 63,
            '6M': 126,
            '1Y': 252
            }

    period_freq = freq[period]
    df_lag = df.shift(period_freq)
    mom = round((df['OPEN'] - df_lag['CLOSE'])/df_lag['CLOSE'], 4)
    mom.index = df['Date'].values
    return mom


def momentum_table(stock_list):
    freq = ['5D', '1M', '3M', '6M', '1Y']
    mom_list = []
    index_list = []
    for item in stock_list:
        index_list.append(item[:-4])
        df = data_reader(item)
        stock_mom = []
        for frequency in freq:
            x = momentum_roc(df, frequency)
            stock_mom.append(x[-1])
        mom_list.append(stock_mom)

    df = pd.DataFrame(mom_list)
    df.index = index_list
    df.columns = freq
    df.name = 'ROC'
    print(df)


if __name__ == '__main__':
    stock_list = data_lister()
    momentum_table(stock_list)
