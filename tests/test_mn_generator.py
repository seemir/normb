# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.mn_generator import MultivariateNormalityGenerator
from tests.test_setup import TestSetup
import pandas as pd
import pytest as pt


class TestMultivariateNormalityGenerator(TestSetup):

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before all tests

        """
        super(TestMultivariateNormalityGenerator, self).setup()
        self.mng = {}
        for name, df in self.dfs.items():
            self.mng.update({name: MultivariateNormalityGenerator(df, digits=5)})

    def test_instances_of_output_is_str_containing_results(self):
        """
        Test that the generate_descriptive_statistics() method produces str objects containing results of all
        normality tests

        """
        normality_tests = ['mardia', 'royston', 'henze-zirkler', 'doornik-hansen', 'energy']
        for mng in self.mng.values():
            results = getattr(mng, 'generate_multivariate_normality_results')()
            assert isinstance(results, str)
            assert all(normality_test in results for normality_test in normality_tests)

    def test_typeerror_raised_when_non_pd_dataframe_passed_into_constructor(self):
        """
        TypeError raised when non - pd.DataFrame passed into constructor

        """
        invalid_dfs = [{}, [], (), 'test', True]
        for invalid_df in invalid_dfs:
            with pt.raises(TypeError):
                mng = MultivariateNormalityGenerator(invalid_df, digits=5)

    def test_typeerror_raised_when_digits_is_not_int(self):
        """
        Test that TypeError is thrown when invalid datatype of digits is passed to
        DescriptiveStatisticsGenerator

        """
        invalid_digits = [{}, [], (), 'test']
        for df in self.dfs.values():
            for invalid_digit in invalid_digits:
                with pt.raises(TypeError):
                    mng = MultivariateNormalityGenerator(df, digits=invalid_digit)

    def test_instance_variables_gets_set_in_constructor(self):
        """
        Test that instance variables, i.e. df, dim and digits gets set when passed through
        constructor

        """
        for i, df in enumerate(self.dfs.values()):
            for j, mng in enumerate(self.mng.values()):
                if i == j:
                    pd.testing.assert_frame_equal(df, mng.df)
                    assert mng.dim == 'col'
                    assert mng.digits == 5
