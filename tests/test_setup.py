# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator


class TestSetup:

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """

        cls.seed = 90210
        cls.dfg = DataFrameGenerator(seed=cls.seed)
        cls.dfs = {method: getattr(cls.dfg, method)() for method in cls.dfg.__getmethods__()}
