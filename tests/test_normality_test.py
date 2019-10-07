# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.multivariate_norm.normality_test import NormalityTest
from source.exceptions.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from tests.test_setup import TestSetup
import pytest as pt


class TestNormalityTest(TestSetup):

    def test_normality_test_cannot_be_instantiated(self):
        """
        Test that the base class (AbstractNormalityTest) cannot be instantiated, i.e. an TypeError
        is thrown

        """
        pt.raises(BaseClassCannotBeInstantiated, NormalityTest)

    def test_abstract_normality_test_cannot_be_instantiated_when_df_is_passed(self):
        """
        Test that the base class (AbstractNormalityTest) cannot be instantiated when df is passed
        through constructor, i.e. an TypeError is thrown

        """
        for df in self.dfs.values():
            with pt.raises(BaseClassCannotBeInstantiated):
                NormalityTest(df=df)
