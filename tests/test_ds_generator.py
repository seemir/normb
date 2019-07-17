# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.ds_generator import DescriptiveStatisticsGenerator
from source.util.abstract_generator import AbstractGenerator
from tests.test_setup import TestSetup
import pandas as pd
import pytest as pt


class TestDescriptiveStatisticsGenerator(TestSetup):

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before all tests

        """
        super(TestDescriptiveStatisticsGenerator, self).setup()
        self.dss = {}
        for name, df in self.dfs.items():
            self.dss.update({name: DescriptiveStatisticsGenerator(df, dim='col', digits=5)})

    def test_ds_generator_is_subclass_of_abstract_generator(self):
        """
        Test that DescriptiveStatisticsGenerator is subclass of AbstractGenerator

        """
        assert isinstance(self.dfg, AbstractGenerator)
        assert issubclass(self.dfg.__class__, AbstractGenerator)

    def test_typeerror_raised_when_non_pd_dataframe_passed_into_constructor(self):
        """
        TypeError raised when non - pd.DataFrame passed into constructor

        """
        invalid_dfs = [{}, [], (), 'test', True]
        for invalid_df in invalid_dfs:
            with pt.raises(TypeError):
                dsg = DescriptiveStatisticsGenerator(invalid_df, dim='col', digits=5)

    def test_typeerror_raised_when_dim_is_not_str(self):
        """
        Test that TypeError is thrown when invalid datatype of dim is passed to
        DescriptiveStatisticsGenerator

        """
        invalid_dims = [{}, [], (), True]
        for df in self.dfs.values():
            for invalid_dim in invalid_dims:
                with pt.raises(TypeError):
                    dsg = DescriptiveStatisticsGenerator(df, dim=invalid_dim, digits=5)

    def test_typeerror_raised_when_digits_is_not_int(self):
        """
        Test that TypeError is thrown when invalid datatype of digits is passed to
        DescriptiveStatisticsGenerator

        """
        invalid_digits = [{}, [], (), 'test']
        for df in self.dfs.values():
            for invalid_digit in invalid_digits:
                with pt.raises(TypeError):
                    dsg = DescriptiveStatisticsGenerator(df, dim='col', digits=invalid_digit)

    def test_instance_variables_gets_set_in_constructor(self):
        """
        Test that instance variables, i.e. df, dim and digits gets set when passed through
        constructor

        """
        for i, df in enumerate(self.dfs.values()):
            for j, dss in enumerate(self.dss.values()):
                if i == j:
                    pd.testing.assert_frame_equal(df, dss.df)
                    assert dss.dim == 'col'
                    assert dss.digits == 5
