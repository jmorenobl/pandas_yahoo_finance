Pandas Yahoo Finance!
=====================

Yahoo Finance! remote data access for Pandas. Since the remote data access to Yahoo Finance! 
was deprecated in the latest pandas-datareader project I wanted to fill the gap with this
implementation.

## Installation

This packages has the following dependencies:
* Pandas>=0.19.2
* Requests>=2.3.0

To install latest version:
```
$ pip install git+https://github.com/jmorenobl/pandas_yahoo_finance.git#egg=pandas_yahoo_finance
```

## Usage

The API is the same that it's found in pandas-datareader. First you need to import the package
with the following command:

```
import pandas_yahoo_finance as pyf
```

Then you can use de Available APIs:

```
# To grab one symbol only. It returns a Pandas data frame
data = pyf.DataReader('^IBEX', '2018-01-01', '2018-06-30')

# To grab more than one symbols at once. It returns a dict with the symbol as key
# and the data frame as the value.
data = pyf.BatchDataReader(['^IBEX', 'TEF.MC'], '2018-01-01', '2018-06-30')
```
