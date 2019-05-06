# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.abstract_generator import AbstractGenerator
import pytest as pt


class TestAbstractGenerator:

    def test_abstract_generator_cannot_be_instantiated(self):
        """
        Test that the base class (AbstractGenerator) cannot be instantiated, i.e. an
        exception is thrown

        """
        pt.raises(Exception, AbstractGenerator)
