# coursera.org / Computational Investing 1
#
# Homework 7
# Author: matsjo
# Date: 20160106

import pandas as pd
import pandas.io.parsers as pd_par
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

NUM_TRADING_DAYS = 252
ls_symbols = ["$SPX"]
valueFile = "value.csv"

value_data = pd_par.read_csv(valueFile, header=None)

value_data.columns = ['year','month','day','value']

portVal = value_data['value']

portVal = portVal / portVal[0]
dailyVal = portVal.copy()


tsu.returnize0(dailyVal)

fdaily_ret = np.mean(dailyVal)
fvol = np.std(dailyVal)
fsharpe = np.sqrt(NUM_TRADING_DAYS) * fdaily_ret / fvol
fcum_ret = portVal[len(portVal) -1]/portVal[0]


# Getting the start and end dates from the .csv file
df_lastrow = len(value_data) - 1
dt_start = dt.datetime( value_data.get_value(0, 'year'), value_data.get_value(0, 'month'), value_data.get_value(0, 'day'), 16 )
dt_end = dt.datetime( value_data.get_value(df_lastrow, 'year'), value_data.get_value(df_lastrow, 'month'), value_data.get_value(df_lastrow, 'day'), 16 )

# Getting market data
dataobj = da.DataAccess('Yahoo',cachestalltime=0)
ls_keys = ['close', 'actual_close']
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

d_data = dict(zip(ls_keys, ldf_data))

temp = d_data['close'].values.copy()
portVal = temp / temp[0,:]

dailyVal = portVal.copy()
tsu.returnize0(dailyVal)

# Calculate statistics
pdaily_ret = np.mean(dailyVal)
pvol = np.std(dailyVal)
psharpe = np.sqrt(NUM_TRADING_DAYS) * pdaily_ret / pvol
pcum_ret = portVal[len(portVal) -1]/portVal[0]


print "Details of the Performance of the portfolio:\n"

print "Date Range: ", dt_start, dt_end
print "\n"

print "Sharpe Ratio of Fund :", fsharpe
print "Sharpe Ratio of", ls_symbols[0],":", psharpe
print "\n"

print "Total Return of Fund :", fcum_ret
print "Total Return of", ls_symbols[0],":", pcum_ret[0]
print "\n"

print "Standard Deviation of Fund :", fvol
print "Standard Deviation of", ls_symbols[0],":", pvol
print "\n"

print "Average Daily Return of Fund :", fdaily_ret
print "Average Daily Return of", ls_symbols[0],":", pdaily_ret
print "\n"
