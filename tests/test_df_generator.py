from normbatt.util.generators.df_generator import DataFrameGenerator
from normbatt.util.generators.abstract_generator import AbstractGenerator
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
        self.dfs = {"normal": self.dfg.normal_data_frame(),
                    "uniform": self.dfg.uniform_data_frame(),
                    "mixed": self.dfg.mixed_data_frame()}

    def test_instances_are_subclass_of_abstract_generator(self):
        """
        Test the DataFrameGenerator instances are subtypes of AbstractGenerator

        """
        assert issubclass(self.dfg.__class__, AbstractGenerator)

    def test_instances_are_instance_and_type_dataframegenerator(self):
        """
        Test for correct DataFrameGenerator type

        """
        assert isinstance(self.dfg, DataFrameGenerator)
        assert type(self.dfg) == DataFrameGenerator

    def test_instances_of_output_distribution_are_instance_and_type_pandas_dataframe(self):
        """
        Test that all df methods in DataFrameGenerator (normal, uniform, mixed) produce
        Pandas dataframes.

        """
        for dataframe in self.dfs.values():
            assert isinstance(dataframe, pd.DataFrame)
            assert type(dataframe) == pd.DataFrame

    def test_raise_typeerror_when_seed_is_not_int(self):
        """
        Test that TypeError is thrown when invalid datatype of seed is passed to
        DataFrameGenerator()

        """
        seeds = [{}, [], (), 'test', True]
        for seed in seeds:
            pt.raises(TypeError, self.dfg, seed)

    def test_seed_gets_set_in_constructor(self):
        """
        Test that seed gets set when passed through constructor

        """
        assert self.dfg.seed == self.seed
        assert self.dfg.seed == 123456789

    def test_seed_always_produces_same_df(self):
        """
        Test that the seed configured produces the same df

        """
        test_seed = 90210
        test_df = DataFrameGenerator(test_seed).uniform_data_frame(sample=(2, 2))
        correct_df = pd.DataFrame(
            np.array([[19.23366508, 92.51010224], [39.57834764, 78.56387572]]))
        pd.testing.assert_frame_equal(test_df, correct_df)

    def test_evaluate_data_type_method_throws_typeerror(self):
        """
        Test that the evaluate_data_type method produces TypeError

        """
        arg = 'test'
        pt.raises(TypeError, self.dfg.evaluate_data_type({arg: list}))

    def test_correct_number_of_calls_made_to_method(self, mocker):
        """
        Mocker of calls to methods in DataFrameGenerator

        """
        methods = ['uniform_data_frame', 'normal_data_frame', 'mixed_data_frame']
        for method in methods:
            mocker.spy(DataFrameGenerator, method)
            dfg = DataFrameGenerator()
            df_method = getattr(dfg, method)()
            assert getattr(DataFrameGenerator, method).call_count == 1
