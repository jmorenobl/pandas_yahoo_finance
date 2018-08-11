import pandas_yahoo_finance as pyf
from datetime import datetime as dt

data = pyf.DataReader('^IBEX', '2018-01-01', '2018-06-30')
print(data)

data = pyf.BatchDataReader(['^IBEX', 'TEF.MC'], '2018-01-01', '2018-06-30')
print(data)