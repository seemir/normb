# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd
import numpy as np


class DataFrameGenerator:

    def __init__(self, seed=None):
        """
        Initiates the class

        Parameters
        ----------
        seed    : int
                  User can set a seed parameter to generate deterministic,
                  non-random output

        """
        try:
            if seed is not None:
                seed = int(seed)
        except Exception:
            raise TypeError(
                "seed must be of type: 'int', got '{}'".format(type(seed).__name__))
        self.seed = seed

    @staticmethod
    def _to_excel(df, filename):
        """
        Method that converts dataframe (df) to Excel

        Parameters
        ----------
        df      : pandas.core.frame.DataFrame
                  dataframe to be converted into excel
        filename: string
                  name of excel file

        """
        engine = 'xlsxwriter'
        with pd.ExcelWriter("{}.xlsx".format(filename), engine=engine) as writer:
            df.to_excel(writer)

    def uniform_data_frame(self, limits=(0, 100), sample=(30, 30), excel=None,
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
        lower, upper = limits
        df = pd.DataFrame(np.random.uniform(lower, upper, sample))

        if excel:
            self._to_excel(df, filename)
        return df

    def normal_data_frame(self, mu=0, sigma=1, sample=(30, 30), excel=None,
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
        df = pd.DataFrame(np.random.normal(mu, sigma, sample))
        if excel:
            self._to_excel(df, filename)
        return df

    def mixed_data_frame(self, mu=0, sigma=1, limits=(0, 100), sample=(30, 30), excel=None,
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
        original_df = self.uniform_data_frame(limits, sample)
        mixed_df = original_df.append(self.normal_data_frame(mu, sigma, sample),
                                      ignore_index=True)
        df = mixed_df.apply(np.random.permutation)
        if excel:
            self._to_excel(df, filename)
        return df
