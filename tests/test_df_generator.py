# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.df_generator import DataFrameGenerator
from normbatt.util.generators.abstract_generator import AbstractGenerator
import pandas as pd
import pytest as pt
import numpy as np
import os


class TestDfGenerator:

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before all tests

        """
        self.seed = 123456789
        self.dfg = DataFrameGenerator(seed=self.seed)
        self.dfs = {'uniform_data_frame': self.dfg.uniform_data_frame(),
                    'normal_data_frame': self.dfg.normal_data_frame(),
                    'mixed_data_frame': self.dfg.mixed_data_frame()}

    def test_instances_are_subclass_of_abstract_generator(self):
        """
        Test the DataFrameGenerator instances are subtypes of AbstractGenerator

        """
        assert issubclass(self.dfg.__class__, AbstractGenerator)

    def test_instances_are_instance_of_dataframe_generator(self):
        """
        Test for correct DataFrameGenerator type

        """
        assert isinstance(self.dfg, DataFrameGenerator)

    def test_instances_of_output_distribution_are_instance_of_pandas_dataframe(self):
        """
        Test that all df methods in DataFrameGenerator (normal, uniform, mixed) produce
        Pandas dataframes.

        """
        for dataframe in self.dfs.values():
            assert isinstance(dataframe, pd.DataFrame)

    def test_raise_typeerror_when_seed_is_not_int(self):
        """
        Test that TypeError is thrown when invalid datatype of seed is passed to
        DataFrameGenerator()

        """
        invalid_seeds = [{}, [], (), 'test', True]
        for seed in invalid_seeds:
            pt.raises(TypeError, self.dfg, seed)

    def test_seed_gets_set_in_constructor(self):
        """
        Test that seed gets set when passed through constructor

        """
        assert self.dfg.seed == self.seed
        assert self.dfg.seed == 123456789

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
            dfg = DataFrameGenerator(self.seed)
            df_method = getattr(dfg, method)()
            assert getattr(DataFrameGenerator, method).call_count == 1

    def test_typeerror_raised_if_non_pd_dataframe_passed_in_to_excel(self):
        """
        TypeError is thrown if non - pd.DataFrame object is passed in to_excel() method

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
        file_dir = 'test_reports/xlsx'
        self.dfg.to_excel(df=input_df, file_dir=file_dir)
        saved_df = pd.read_excel(file_dir + '/' + os.listdir(file_dir)[-1], index_col=0)
        pd.testing.assert_frame_equal(saved_df, input_df)

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
        for idx, column in df.iteritems():
            assert np.mean(column.to_list()) == pt.approx(0, abs=1)

        for idx, row in df.iterrows():
            assert np.mean(row.to_list()) == pt.approx(0, abs=1)
