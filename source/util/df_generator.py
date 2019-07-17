# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.abstract_generator import AbstractGenerator
import pandas as pd
import numpy as np
import datetime
import os


class DataFrameGenerator(AbstractGenerator):
    """
    Class that generates pandas.DataFrame with values of a given distribution, i.e. uniform,
    normal or mixed.

    """

    def __init__(self, seed, sample):
        """
        Initiates the class

        Parameters
        ----------
        seed    : int
                  User can set a seed parameter to generate deterministic, non-random output

        """
        self.evaluate_data_type({seed: int, sample: tuple})
        super().__init__(seed=seed, sample=sample)

    def to_excel(self, df, file_dir="reports/xlsx", header=True, index=True):
        """
        Method that converts dataframe (df) to Excel

        Parameters
        ----------
        df      : pandas.DataFrame
                  dataframe to be converted into excel
        file_dir: str
                  directory to save the file
        header  : bool
                  Write out the column names
        index   : bool
                  Write row names

        """
        self.evaluate_pd_dataframe(df)
        self.evaluate_data_type({file_dir: str})

        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        filepath = os.path.join(file_dir, "ExcelDataFrame_" + local_time + ".xlsx")

        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        df.to_excel(filepath, header=header, index=index)

    def uniform_data_frame(self, limits=(-1, 1), excel=None):
        """
        Method that produces a df containing uniformly distributed floating point values between
        'limits' and of dimensions defined in 'sample' argument.

        Parameters
        ----------
        limits  : tuple
                  (lower, upper) limit of values to be generated in df
        excel   : bool
                  indicating if one wants to output to excel

        Returns
        -------
        Out     : pandas.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)
        self.evaluate_data_type({limits: tuple})

        lower, upper = limits
        df = pd.DataFrame(np.random.uniform(lower, upper, self.sample))

        if excel:
            self.to_excel(df)
        return df

    def normal_data_frame(self, mu=0, sigma=1, excel=None):
        """
        Method that produces a df containing normally distributed floating point values with mean
        equal 'mu' and st.dev equal 'sigma' and dimensions defined by 'sample'.

        Parameters
        ----------
        mu      : integer, float
                  mean value
        sigma   : integer, float
                  standard deviation
        excel   : bool
                  indicating if one wants to output to excel

        Returns
        -------
        Out     : pandas.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)
        self.evaluate_data_type({mu: int, sigma: int})

        df = pd.DataFrame(np.random.normal(mu, sigma, self.sample))

        if excel:
            self.to_excel(df)
        return df

    def mixed_data_frame(self, mu=0, sigma=1, limits=(-1, 1), excel=None):
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
        excel   : bool
                  indicating if one wants to output to excel

        Returns
        -------
        Out     : pandas.DataFrame
                  n x 1 (if sample is integer) or n x m (if sample is tuple) dimensional df

        """
        np.random.seed(self.seed)
        self.evaluate_data_type({mu: int, sigma: int, limits: tuple})

        original_df = self.uniform_data_frame(limits)
        mixed_df = original_df.append(self.normal_data_frame(mu, sigma),
                                      ignore_index=True)
        df = mixed_df.apply(np.random.permutation).head(self.sample[0])

        if excel:
            self.to_excel(df)
        return df
