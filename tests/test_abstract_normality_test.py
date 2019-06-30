# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.multivariate_norm.abstract_normality_test import AbstractNormalityTest
from tests.test_setup import TestSetup
import pytest as pt


class TestAbstractNormalityTest(TestSetup):

    def test_abstract_normality_test_cannot_be_instantiated(self):
        """
        Test that the base class (AbstractNormalityTest) cannot be instantiated, i.e. an
        TypeError is thrown

        """
        for df in self.dfs.values():
            with pt.raises(TypeError):
                ab = AbstractNormalityTest(df=df)
