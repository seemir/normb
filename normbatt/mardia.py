# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.df_generator import DataFrameGenerator
from sklearn.preprocessing import scale
import pandas as pd


class Mardia:
    """
    Runs the multivariate normality test as described by Mardia, K. V. (1970)

    """

    def __init__(self, df, cov=True, tol=1e-25):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  df to be analysed
        cov     : bool
                  indicating if adjusted covariance matrix is to be used
        tol     : float
                  the tolerance for detecting linear dependencies in the columns of df

        """
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df).__name__))

        DataFrameGenerator.evaluate_data_type({cov: bool, tol: float})

        self.df = df
        self.cov = cov
        self.tol = tol
        self.n = self.df.shape[0]
        self.p = self.df.shape[1]

    @staticmethod
    def scale_data(df):
        """
        Method that centers the columns of a numeric df.

        Parameters
        ----------
        df      : pandas.DataFrame
                  dataframe to be centered

        Returns
        -------
        Out     : pandas.DataFrame
                  centered dataframe

        """
        return scale(df)

    def calculate_sigma(self):
        """
        Calculated adjusted or non-adjusted covariance matrix of df

        Returns
        -------
        Out     : pandas.DataFrame
                  covariance matrix as pandas.DataFrame

        """
        return self.df.cov().multiply(((self.n - 1) / self.n)) if self.cov else self.df.cov()
