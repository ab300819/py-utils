# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib import ticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.dates import MonthLocator
from matplotlib.dates import MONTHLY
import datetime
import pylab

day_line_file = ''
stock_b_code = '000001'
MA1 = 10
MA2 = 50

start_date = datetime.date(2017, 1, 16)
end_date = datetime.date(2017, 1, 20)


def moving_average(data, n):
    result = np.cumsum(np.insert(data, 0, 0))
    return (result[n:] - result[:-n]) / n


def read_stk_data(root_path, stock_code, start_day, end_day):
    return_data = pd.DataFrame()
