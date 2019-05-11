# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.df_generator import DataFrameGenerator
from normbatt.normality_battery import NormalityBattery

if __name__ == '__main__':
    seed = 90210
    ini_df = DataFrameGenerator(seed)
    results = NormalityBattery(ini_df.mixed_data_frame(excel=True))
    results.print_report(ds=True)