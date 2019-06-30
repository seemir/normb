# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from normbatt.normality_battery import NormalityBattery


class TestSetup:

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """

        cls.seed = 90210
        cls.dfg = DataFrameGenerator(seed=cls.seed)
        cls.dfs = {method: getattr(cls.dfg, method)() for method in cls.dfg.__getmethods__()}
        cls.nbs = {method: NormalityBattery(df) for method, df in cls.dfs.items()}
