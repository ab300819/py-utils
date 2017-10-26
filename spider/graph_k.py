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
stock_b_code=''
MA1=10
MA2=50