# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator


class TestSetup:

    def setup(self):
        """
        Executed before all tests

        """
        self.seed = 90210
        self.dfg = DataFrameGenerator(seed=self.seed)
        self.dfs = {'uniform_data_frame': self.dfg.uniform_data_frame(),
                    'normal_data_frame': self.dfg.normal_data_frame(),
                    'mixed_data_frame': self.dfg.mixed_data_frame()}
