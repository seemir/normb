# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from tests.test_setup import TestSetup
import pandas as pd
import pytest as pt
import numpy as np
import os


class TestDataFrameGenerator(TestSetup):

    def test_raise_typeerror_when_seed_is_not_int(self):
        """
        Test that TypeError is thrown when invalid datatype of seed is passed to
        DataFrameGenerator()

        """
        invalid_seeds = [{}, [], (), 'test', True]
        for seed in invalid_seeds:
            pt.raises(TypeError, self.dfg, seed)

    def test_seed_always_produces_same_df(self):
        """
        Test that the seed configured produces the same df

        """
        test_seed = 90210
        test_df = DataFrameGenerator(test_seed).uniform_data_frame(sample=(2, 2), limits=(0, 100))
        correct_df = pd.DataFrame(
            np.array([[19.23366508, 92.51010224], [39.57834764, 78.56387572]]))
        pd.testing.assert_frame_equal(test_df, correct_df)

    def test_correct_number_of_calls_made_to_method(self, mocker):
        """
        Mocker of calls to methods in DataFrameGenerator

        """
        methods = self.dfs.keys()
        for method in methods:
            mocker.spy(DataFrameGenerator, method)
            df_method = getattr(self.dfg, method)()
            assert getattr(DataFrameGenerator, method).call_count == 1

    def test_typeerror_raised_when_non_pd_dataframe_passed_in_to_excel(self):
        """
        TypeError is thrown when non - pd.DataFrame object is passed in to_excel() method

        """
        invalid_dfs = [{}, [], (), 'test', True]
        for invalid_df in invalid_dfs:
            with pt.raises(TypeError):
                self.dfg.to_excel(invalid_df)

    def test_to_excel_produces_excel_file_with_dataframe(self):
        """
        Static to_excel() method produces excel file with dataframe

        """
        input_df = pd.DataFrame(np.random.rand(30, 30))
        file_dir = 'reports/xlsx'
        self.dfg.to_excel(df=input_df, file_dir=file_dir)
        saved_df = pd.read_excel(file_dir + '/' + os.listdir(file_dir)[-1], index_col=0)
        pd.testing.assert_frame_equal(saved_df, input_df)

    def test_os_error_is_thrown_when_dir_cannot_be_created(self):
        """
        OSError raised when invalid file_dir is passed to to_excel() method

        """
        input_df = pd.DataFrame(np.random.rand(30, 30))
        file_dir = '._?`/1234'  # Invalid dir name
        with pt.raises(OSError):
            self.dfg.to_excel(df=input_df, file_dir=file_dir)

    def test_correct_dimensions_in_produced_df(self):
        """
        Shape of df produced are same as configured

        """
        # Default case, 30 x 30
        for df in self.dfs.values():
            assert df.shape == (30, 30)
            assert np.prod(df.shape) == 900

        # Customized case 100 x 100
        df = self.dfg.normal_data_frame(sample=(100, 100))
        assert df.shape == (100, 100)
        assert np.prod(df.shape) == 10000

    def test_not_possible_to_configure_negative_dimensions(self):
        """
        Negative dimensions are not allowed

        """
        with pt.raises(ValueError):
            self.dfg.normal_data_frame(sample=(-100, 100))

    def test_normal_data_frame_produces_data_with_mean_close_to_value(self):
        """
        Data in dataframe produced by normal_data_frame() have mean close to configured mean value

        """
        # Default case, mean = 0
        df = self.dfs['normal_data_frame']
        for i, column in df.iteritems():
            assert np.mean(column.to_list()) == pt.approx(0, abs=1)

        for i, row in df.iterrows():
            assert np.mean(row.to_list()) == pt.approx(0, abs=1)

    def test_to_excel_from_df_method(self):
        """
        Possible to save produced df to excel using excel=True argument in df methods, i.e.
        uniform_data_frame(), normal_data_frame() and mixed_data_frame()

        """
        file_dir = 'reports/xlsx'
        for method in self.dfs.keys():
            input_df = getattr(self.dfg, method)(excel=True)
            saved_df = pd.read_excel(file_dir + '/' + os.listdir(file_dir)[-1], index_col=0)
            pd.testing.assert_frame_equal(saved_df, input_df)
