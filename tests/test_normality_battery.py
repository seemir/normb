# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.normality_battery import NormalityBattery
from source.util.df_generator import DataFrameGenerator
from tests.test_setup import TestSetup
import pytest as pt
import pandas as pd
import os


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

    def test_valueerror_raised_when_less_than_eight_observational_df_passed(self):
        """
        Test that ValueError is raised when less than 8 observational df is passed through
        the NormalityBattery() class.

        """
        for method in self.dfs.keys():
            test_df = getattr(DataFrameGenerator(seed=90210, sample=(2, 2)), method)()
            with pt.raises(ValueError):
                NormalityBattery(test_df)

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
        print_univariate_normality etc.) produces str object with correct
        parameters

        """
        for nb in self.nbs.values():
            for method in nb.__getmethods__():
                nb_results = getattr(nb, method)()
                assert all(param in nb_results for param in self.params[method])
                isinstance(nb_results, str)

    def test_os_error_in_print_report(self):
        """
        OSError raised when invalid file_dir is passed to print_report() method

        """
        invalid_file_dir = '._?`/1234'  # Invalid dir name
        for nb in self.nbs.values():
            with pt.raises(OSError):
                nb.print_report(file_dir=invalid_file_dir)

    def test_dir_gets_created_for_reports(self):
        """
        Test that directory gets produced when running print_report() method

        """
        list(self.nbs.values())[0].print_report()
        assert os.path.isdir('reports/txt')

    def test_ds_included_in_report(self):
        """
        Test that the descriptive statistics is included when setting ds=True in print_reports()
        method

        """
        list(self.nbs.values())[0].print_report(ds=True)
        with open(self.file_dir + '/' + os.listdir(self.file_dir)[-1], 'r') as file:
            data = file.read().replace('\n', '')
            assert all(param in data for param in self.params['print_descriptive_statistics'])

    def test_ds_not_included_in_report(self):
        """
        Test that the descriptive statistics is not included in report when ds!=True in
        print_reports() method

        """
        self.test_dir_gets_created_for_reports()
        with open(self.file_dir + '/' + os.listdir(self.file_dir)[-1], 'r') as file:
            data = file.read().replace('\n', '')
            assert all(param not in data for param in self.params)
