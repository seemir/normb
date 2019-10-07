# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exceptions.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.exceptions.only_numeric_df_accepted import OnlyNumericDfAccepted
from source.util.multivariate_normality import MultivariateNormality
from source.util.descriptive_statistics import DescriptiveStatistics
from source.util.univariate_normality import UnivariateNormality
from source.util.result_generator import ResultGenerator
from source.util.generator import Generator
from tests.test_setup import TestSetup

import pandas as pd
import pytest as pt


class TestGenerators(TestSetup):

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before all tests

        """
        super(TestGenerators, self).setup()
        self.generators = [DescriptiveStatistics,
                           UnivariateNormality,
                           MultivariateNormality,
                           ResultGenerator]

    def test_generator_cannot_be_instantiated(self):
        """
        Test Generator class, i.e. the abstract class cannot be instantiated

        """
        with pt.raises(BaseClassCannotBeInstantiated):
            Generator()

    def test_all_generators_are_subclass_of_generator(self):
        """
        Test that all generators are subclasses of Generator

        """
        for df in self.dfs.values():
            for generator in self.generators:
                if generator != ResultGenerator:
                    assert isinstance(generator(df), Generator)
                    assert issubclass(generator(df).__class__, Generator)
                else:
                    assert isinstance(generator(df, mn='test', un='test'), Generator)
                    assert issubclass(generator(df, mn='test', un='test').__class__,
                                      Generator)

    @pt.mark.parametrize("invalid_df", [{}, [], (), 'test', True])
    def test_typeerror_raised_when_non_pd_data_frame_passed_into_constructor(self, invalid_df):
        """
        TypeError raised when non - pd.DataFrame passed into constructor

        """
        for generator in self.generators:
            with pt.raises(TypeError):
                generator(df=invalid_df)

    def test_only_numeric_df_accepted_into_generators(self):
        """
        NonNumericDfNotAccepted raised when non numeric df passed into contructor

        """
        non_numeric_df = pd.DataFrame([[-1, 0.57127751], ['test', True]])
        for generator in self.generators:
            with pt.raises(OnlyNumericDfAccepted):
                if generator != ResultGenerator:
                    generator(non_numeric_df)
                else:
                    generator(non_numeric_df, mn='test', un='test')

    @pt.mark.parametrize("invalid_dim", [{}, [], (), True])
    def test_typeerror_raised_when_dim_is_not_str(self, invalid_dim):
        """
        Test that TypeError is thrown when invalid datatype of dim is passed to a generator

        """
        for df in self.dfs.values():
            for generator in self.generators:
                with pt.raises(TypeError):
                    generator(df, dim=invalid_dim)

    @pt.mark.parametrize("invalid_digit", [{}, [], (), 'test'])
    def test_typeerror_raised_when_digits_is_not_int(self, invalid_digit):
        """
        Test that TypeError is thrown when invalid datatype of digits is passed to a
        generator

        """

        for df in self.dfs.values():
            for generator in self.generators:
                with pt.raises(TypeError):
                    generator(df, digits=invalid_digit)

    def test_instance_variables_gets_set_in_constructor(self):
        """
        Test that instance variables, i.e. df, dim and digits gets set when passed through
        constructor

        """
        for i, df in enumerate(self.dfs.values()):
            for j, generator in enumerate(self.generators):
                if i == j:
                    generator = generator(df)
                    pd.testing.assert_frame_equal(df, generator.df)
                    assert generator.dim == 'col'
                    assert generator.digits == 5
