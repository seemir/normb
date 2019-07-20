# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.df_generator import DataFrameGenerator
from source.normality_battery import NormalityBattery


class TestSetup:

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """

        cls.seed = 90210
        cls.file_dir = 'reports/txt'
        cls.dfg = DataFrameGenerator(seed=cls.seed, size=(20, 20))
        cls.dfs = {method: getattr(cls.dfg, method)() for method in cls.dfg.__getmethods__()}
        cls.nbs = {method: NormalityBattery(df) for method, df in cls.dfs.items()}
        cls.params = dict(zip(list(cls.nbs.values())[0].__getmethods__(),
                              [['mean', 'median', 'variance', 'stdev', 'kurtosis', 'skewness',
                                'min', 'max'],
                               ['t1', 'p-value (t1)', 't2', 'p-value (t2)', 'mardia', 'royston',
                                'henze-zirkler', 'doornik-hansen', 'energy'],
                               ['jb', 'p-value (jb)', 'k2', 'p-value (k2)', 'ks', 'p-value (ks)',
                                'sw', 'p-value (sw)']
                               ]))
