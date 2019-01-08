# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from df_generator import DataFrameGenerator
import pandas as pd


class NormalityBattery:

    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'")
        self.df = df

    def get_dimensions(self):
        return self.df.shape()

    def check_normality_in_rows(self):
        pass

    def check_normality_in_columns(self):
        pass
