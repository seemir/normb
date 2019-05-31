# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from normbatt.util.time_print import time_progress_print, time_print
from normbatt.normality_battery import NormalityBattery
import datetime

df = DataFrameGenerator(seed=90210)
methods = ['uniform_data_frame', 'normal_data_frame', 'mixed_data_frame']
now = datetime.datetime.now()

time_print("running", "check_normb", now)

for method in methods:
    print("starting method: " + method + "()")
    nb = NormalityBattery(getattr(df, method)(sample=(1000, 100)))
    nb.print_report()
    time_progress_print("finished", method, now)

time_print("completed", "check_normb", datetime.datetime.now())
