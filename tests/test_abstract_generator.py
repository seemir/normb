# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.abstract_generator import AbstractGenerator
import pytest as pt


class TestAbstractGenerator:

    def test_abstract_generator_cannot_be_instantiated(self):
        """
        Test that the base class (AbstractGenerator) cannot be instantiated, i.e. an
        TypeError is thrown

        """
        with pt.raises(TypeError):
            ag = AbstractGenerator()

    def test_access_static_evaluate_pd_dataframe_method(self):
        """
        Test that it is possible to access the static evaluate_pd_dataframe() method without
        instantiating the AbstractGenerator class

        """
        invalid_objects = ['test', [], (), {}, True, 90210, 90210.0]
        for invalid_object in invalid_objects:
            with pt.raises(TypeError):
                AbstractGenerator.evaluate_pd_dataframe(invalid_object)

    def test_access_static_evaluate_data_type_method(self):
        """
        Test that it is possible to access the static evaluate_data_type() method without
        instantiating the AbstractGenerator class

        """
        invalid_objects = ['test', (), {}, True, 90210, 90210.0]
        valid_type = list
        for invalid_object in invalid_objects:
            with pt.raises(TypeError):
                AbstractGenerator.evaluate_data_type({invalid_object: valid_type})
