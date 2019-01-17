from normbatt.df_generator import DataFrameGenerator
import numpy as np
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

    def test_dataframe_seed_type_error(self):
        """
        Test that TypeError is thrown when invalid datatype seed is passed to
        DataFrameGenerator()

        """
        seeds = [{}, [], (), 'test', True]
        for seed in seeds:
            pt.raises(TypeError, self.dfg, seed)

    def test_seed(self):
        """
        Test that seed is configured

        """
        assert self.dfg.seed == self.seed
        assert self.dfg.seed == 123456789

    def test_seed_produces_same_df(self):
        """
        Test that the seed configured produces the same df

        """
        test_seed = 90210
        test_df = DataFrameGenerator(test_seed)
        test_df = np.array(test_df.uniform_data_frame(sample=(2, 2)))
        correct_df = np.array([[19.23366508, 92.51010224], [39.57834764, 78.56387572]])
        pt.approx(correct_df, test_df)

    def test_evaluate_data_type(self):
        """
        Test that the evaluate_data_type method produces TypeError

        """
        arg = 'test'
        pt.raises(TypeError, self.dfg.evaluate_data_type({arg: list}))

    def test_mocker(self, mocker):
        """
        Mocker of calls to methods in DataFrameGenerator

        """
        methods = ['uniform_data_frame', 'normal_data_frame', 'mixed_data_frame']
        for method in methods:
            mocker.spy(DataFrameGenerator, method)
            df = DataFrameGenerator()
            df_method = getattr(df, method)()
            assert getattr(DataFrameGenerator, method).call_count == 1
