# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from normbatt.normality_battery import NormalityBattery
import datetime

df = DataFrameGenerator(seed=90210)
methods = ['uniform_data_frame', 'normal_data_frame', 'mixed_data_frame']
now = datetime.datetime.now()


for method in methods:
    print("starting method: " + method + "()")
    nb = NormalityBattery(getattr(df, method)(sample=(1000, 100)))
    nb.print_report()
