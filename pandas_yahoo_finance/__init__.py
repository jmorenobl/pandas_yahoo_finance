import re
import pandas as pd
import requests

from io import StringIO
from datetime import datetime


__all__ = ['DataReader', 'BatchDataReader']


def get_page_data(symbol):
    def get_cookie_value(r):
        return {'B': r.cookies['B']}

    url = "https://finance.yahoo.com/quote/{}/".format(symbol)
    payload = {'p': symbol}
    response = requests.get(url, params=payload)
    cookie = get_cookie_value(response)

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = response.content.decode('unicode-escape').strip().replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    def split_crumb_store(v):
        return v.split(':')[2].strip('"')

    def find_crumb_store(lines):
        # Looking for
        # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
        for l in lines:
            if re.findall(r'CrumbStore', l):
                return l
        print("Did not find CrumbStore")

    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(url, payload, cookie):
    response = requests.get(url, params=payload, cookies=cookie)
    return StringIO(response.text)


def setup_params(symbol, start, end, interval):
    cookie, crumb = get_cookie_crumb(symbol)

    payload = {
        'period1': int(start.timestamp()),
        'period2': int(end.timestamp()),
        'interval': interval,
        'events': 'history',
        'crumb': crumb
    }

    return payload, cookie


def get_symbol_data(start, end, url, payload, cookie):
    stock_data = get_data(url, payload, cookie)

    dates = pd.date_range(start, end)
    df = pd.DataFrame(index=dates)
    df_temp = pd.read_csv(stock_data,
                          index_col='Date',
                          parse_dates=True,
                          na_values=['null'])

    df = df.join(df_temp, how='left')
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)

    return df


def DataReader(symbol, start, end, interval='1d'):
    if not isinstance(start, datetime):
        raise Exception('start parameter must be an instance of datetime.datetime')

    if not isinstance(end, datetime):
        raise Exception('end parameter must be an instance of datetime.datetime')

    payload, cookie = setup_params(symbol, start, end, interval)

    url = "https://query1.finance.yahoo.com/v7/finance/download/{}".format(symbol)

    return get_symbol_data(start, end, url, payload, cookie)


def BatchDataReader(symbols, start, end, interval='1d'):
    if not isinstance(symbols, list) and not isinstance(symbols, tuple):
        raise Exception("symbols must be a list of symbols. i.e. ['APPL', 'GOOG']")

    if not isinstance(start, datetime):
        raise Exception('start parameter must be an instance of datetime.datetime')

    if not isinstance(end, datetime):
        raise Exception('end parameter must be an instance of datetime.datetime')

    payload, cookie = setup_params(symbols[0], start, end, interval)

    symbols_dict = {}
    for symbol in symbols:
        url = "https://query1.finance.yahoo.com/v7/finance/download/{}".format(symbol)

        symbols_dict[symbol] = get_symbol_data(start, end, url, payload, cookie)

    return symbols_dict
