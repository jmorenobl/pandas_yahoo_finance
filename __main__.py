import pandas_yahoo_finance as pyf
from datetime import datetime as dt

data = pyf.DataReader('^IBEX', dt(2018, 1, 1), dt(2018, 6,30))
print(data)

data = pyf.BatchDataReader(['^IBEX', 'TEF.MC'], dt(2018, 1, 1), dt(2018, 6,30))
print(data)