from normbatt.df_generator import DataFrameGenerator
import pandas as pd
import pytest as pt


class TestDfGenerator:

    @pt.fixture(autouse=True)
    def setup(self):
        """
        Executed before all tests

        """
        self.seed = 123456789
        self.dfg = DataFrameGenerator(self.seed)
        self.drs = {DataFrameGenerator.normal_data_frame: self.dfg.normal_data_frame(),
                    DataFrameGenerator.uniform_data_frame: self.dfg.uniform_data_frame(),
                    DataFrameGenerator.mixed_data_frame: self.dfg.mixed_data_frame()}

    def test_instance_dataframegenerator(self):
        """
        Test for correct DataFrameGenerator type

        """
        assert isinstance(self.dfg, DataFrameGenerator)

    def test_instance_dataframe(self):
        """
        Test that all df methods in DataFrameGenerator (normal, uniform, mixed) produce
        Pandas dataframes.

        """
        for dataframe in self.drs.values():
            assert isinstance(dataframe, pd.DataFrame)

    def test_dataframe_seed_type(self):
        """
        Test that TypeError is thrown when invalid datatype seed is passed to DataFrameGenerator()

        """
        seeds = [{}, [], (), 'test', True]
        for seed in seeds:
            pt.raises(TypeError, self.dfg, seed)

    def test_seed(self):
        """
        Test that seed is configured

        """
        assert self.dfg.seed == self.seed
