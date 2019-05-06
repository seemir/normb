# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.abstract_generator import AbstractGenerator
import pandas as pd
import numpy as np


class DataFrameGenerator(AbstractGenerator):
    """
    Class that generates pandas.DataFrame with values of a given distribution, i.e. uniform,
    normal or mixed.

    """

    def __init__(self, seed=None):
        """
        Initiates the class

        Parameters
        ----------
        seed    : int
                  User can set a seed parameter to generate deterministic, non-random output

        """
        self.evaluate_data_type({seed: int})
        super().__init__(seed=seed)

    def to_excel(self, df=None, filename="ExcelDataFrame.xlsx"):
        """
        Method that converts dataframe (df) to Excel

        Parameters
        ----------
        df      : pandas.core.frame.DataFrame
                  dataframe to be converted into excel
        filename: string
                  name of excel file

        """
        self.evaluate_data_type({df: pd.DataFrame, filename: str})

        engine = 'xlsxwriter'
        with pd.ExcelWriter("{}.xlsx".format(filename), engine=engine) as writer:
            df.to_excel(writer)

    def uniform_data_frame(self, limits=(-1, 1), sample=(30, 30), excel=None,
                           filename='ExcelDF.xlsx'):
        """
        Method that produces a df containing uniformly distributed floating point values between
        'limits' and of dimensions defined in 'sample' argument.

        Parameters
        ----------
        limits  : tuple
                  (lower, upper) limit of values to be generated in df
        sample  : tuple of integers, integer
                  dimensions or range of numbers in generated df, default is (30, 30)
        excel   : boolean
                  indicating if one wants to output to excel
        filename: string
                  name of excel file

        Returns
        -------
        Out     : pandas.core.frame.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)

        args = {limits: tuple, sample: tuple, filename: str}
        self.evaluate_data_type(args)

        lower, upper = limits
        df = pd.DataFrame(np.random.uniform(lower, upper, sample))

        if excel:
            self.to_excel(df, filename)
        return df

    def normal_data_frame(self, mu=0, sigma=1, sample=(30, 30), excel=False,
                          filename='ExcelDF.xlsx'):
        """
        Method that produces a df containing normally distributed floating point values with mean
        equal 'mu' and st.dev equal 'sigma' and dimensions defined by 'sample'.

        Parameters
        ----------
        mu      : integer, float
                  mean value
        sigma   : integer, float
                  standard deviation
        sample  : tuple of integers, integer
                  dimensions of df to be produced, default is (30, 30)
        excel   : boolean
                  indicating if one wants to output to excel
        filename: string
                  name of excel file

        Returns
        -------
        Out     : pandas.core.frame.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)

        args = {mu: int, sigma: int, sample: tuple, filename: str}
        self.evaluate_data_type(args)

        df = pd.DataFrame(np.random.normal(mu, sigma, sample))
        if excel:
            self.to_excel(df, filename)
        return df

    def mixed_data_frame(self, mu=0, sigma=1, limits=(-1, 1), sample=(30, 30), excel=None,
                         filename='ExcelDF.xlsx'):
        """
        Generates a df with an equal mix of uniformly and normally distributed values.

        Parameters
        ----------
        mu      : integer, float
                  mean value
        sigma   : integer, float
                  standard deviation
        limits  : tuple
                  (lower, upper) limit of values to be generated in df
        sample  : tuple of integers, integer
                  dimensions of df to be produced, default is (30, 30)
        excel   : boolean
                  indicating if one wants to output to excel
        filename: string
                  name of excel file

        Returns
        -------
        Out     : pandas.core.frame.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)

        args = {mu: int, sigma: int, limits: tuple, sample: tuple, filename: str}
        self.evaluate_data_type(args)

        original_df = self.uniform_data_frame(limits, sample)
        mixed_df = original_df.append(self.normal_data_frame(mu, sigma, sample),
                                      ignore_index=True)
        df = mixed_df.apply(np.random.permutation).head(sample[0])
        if excel:
            self.to_excel(df, filename)
        return df
