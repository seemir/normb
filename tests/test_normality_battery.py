# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.normality_battery import NormalityBattery
from normbatt.util.generators.df_generator import DataFrameGenerator
import pytest as pt


class TestNormalityBattery:

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before every test

        """
        self.seed = 90210
        self.dfg = DataFrameGenerator(seed=self.seed)
        self.nb_uniform = NormalityBattery(self.dfg.uniform_data_frame())
        self.nb_normal = NormalityBattery(self.dfg.normal_data_frame())
        self.nb_mixed = NormalityBattery(self.dfg.mixed_data_frame())

    def test_all_dfg_are_of_instance_dataframegenerator(self):
        """
        Test correct dataframe generator type is created

        """
        assert isinstance(self.dfg, DataFrameGenerator)

    def test_all_normalitybattery_instances_are_of_type_normalitybattery(self):
        """
        Test that all the normality battery instances are of type NormalityBattery()

        """
        nbs = [self.nb_uniform, self.nb_normal, self.nb_mixed]
        for nb in nbs:
            assert isinstance(nb, NormalityBattery)

    def test_typeerror_raised_when_invalid_data_type_is_instantiated(self):
        """
        Test that TypeError is raised if invalid data type is instantiated

        """""
        dfs = [90210, 'test', True]
        for df in dfs:
            pt.raises(TypeError, NormalityBattery, df)