# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exceptions.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.assertor import Assertor
import pytest as pt


class TestAssertor:

    def test_assertor_cannot_be_instantiated(self):
        """
        Test that the base class (Assertor) cannot be instantiated, i.e. an
        BaseClassCannotBeInstantiated exception is thrown

        """
        with pt.raises(BaseClassCannotBeInstantiated):
            Assertor()

    @pt.mark.parametrize("invalid_object", ['test', [], (), {}, True, 90210, 90210.0])
    def test_access_static_evaluate_pd_data_frame_method(self, invalid_object):
        """
        Test that it is possible to access the static evaluate_pd_dataframe() method without
        instantiating the Assertor class

        """
        with pt.raises(TypeError):
            Assertor.evaluate_pd_dataframe(invalid_object)

    @pt.mark.parametrize("invalid_object", ['test', (), {}, True, 90210, 90210.0])
    def test_access_static_evaluate_data_type_method(self, invalid_object):
        """
        Test that it is possible to access the static evaluate_data_type() method without
        instantiating the Assertor class

        """
        valid_type = list
        with pt.raises(TypeError):
            Assertor.evaluate_data_type({invalid_object: valid_type})
