# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.normality_battery import NormalityBattery
from normbatt.util.df_generator import DataFrameGenerator
from tests.test_setup import TestSetup
import pytest as pt
import pandas as pd


class TestNormalityBattery(TestSetup):

    def test_all_dfg_are_of_instance_dataframegenerator(self):
        """
        Test correct dataframe generator type is created

        """
        assert isinstance(self.dfg, DataFrameGenerator)

    def test_all_normalitybattery_instances_are_of_type_normalitybattery(self):
        """
        Test that all the normality battery instances are of type NormalityBattery()

        """
        for nb in self.nbs.values():
            assert isinstance(nb, NormalityBattery)

    def test_typeerror_raised_when_invalid_data_type_is_instantiated(self):
        """
        Test that TypeError is raised if invalid data type is instantiated

        """""
        dfs = [90210, 'test', True]
        for df in dfs:
            pt.raises(TypeError, NormalityBattery, df)

    def test_df_gets_instantiated_when_passed_through_nb_constructor(self):
        """
        Test that df gets set when passed through the constructor

        """
        for i, df in enumerate(self.dfs.values()):
            for j, nb in enumerate(self.nbs.values()):
                if i == j:
                    pd.testing.assert_frame_equal(df, nb.df)

    def test_printing_methods(self):
        """
        Test that all the printing methods (print_descriptive_statistics,
        print_univariate_normality etc.) produces str object

        """

        for nb in self.nbs.values():
            for method in nb.__getmethods__():
                nb_results = getattr(nb, method)()
                isinstance(nb_results, str)
