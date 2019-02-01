# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.df_generator import DataFrameGenerator
from sklearn.preprocessing import scale
from scipy.stats import chi2, norm
import pandas as pd
import numpy as np


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

        """
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df).__name__))

        DataFrameGenerator.evaluate_data_type({cov: bool})

        self.df = df
        self.cov = cov
        self.tol = tol
        self.n = self.df.shape[0]
        self.p = self.df.shape[1]

    def center_data(self):
        """
        Method that centers the columns of a numeric df.

        Returns
        -------
        Out     : pandas.DataFrame
                  centered dataframe

        """
        return pd.DataFrame(scale(self.df, with_std=False))

    def calculate_sigma(self):
        """
        Calculated adjusted or non-adjusted covariance matrix of df

        Returns
        -------
        Out     : pandas.DataFrame
                  covariance matrix as pandas.DataFrame

        """
        return self.df.cov().multiply(((self.n - 1) / self.n)) if self.cov else self.df.cov()

    def calculate_d(self):
        """
        Calculates the D-matrix

        Returns
        -------
        Out     : pandas.DataFrame
                  D matrix as pandas.DataFrame

        """
        center = self.center_data().to_numpy()
        invers = np.linalg.inv(self.calculate_sigma())
        transp = np.matrix.transpose(center)
        return pd.DataFrame(center @ invers @ transp)

    def calculate_g_coeff(self):
        """
        Calculate the g coefficients

        Returns
        -------
        Out     : dictionary
                  dict of g coefficients

        """
        d = self.calculate_d().to_numpy()
        g1 = np.sum(np.power(d, 3)) / self.n ** 2
        g2 = np.sum(np.diagonal(np.power(d, 2))) / self.n
        return {'g1': g1, 'g2': g2}

    def get_df(self):
        """
        Get the degrees of freedom

        Returns
        -------
        Out     : int
                  the degrees of freedom

        """
        return self.p * (self.p + 1) * (self.p + 2) / 6

    def get_k(self):
        """
        Get k

        Returns
        -------
        Out     : int
                  k

        """
        return ((self.p + 1) * (self.n + 1) * (self.n + 3)) / (
                self.n * ((self.n + 1) * (self.p + 1) - 6))

    def print_results(self):
        """
        Print the finals results of the Mardia multivariate test

        Returns
        -------
        Out     : tuple
                  (skew, p_skew, kurt, p_kurt)

        """
        if self.n < 20:
            skew = self.n * self.get_k() * self.calculate_g_coeff()['g1'] / 6
            p_skew = 1 - chi2.pdf(skew, self.get_df())
        else:
            skew = self.n * self.calculate_g_coeff()['g1'] / 6
            p_skew = 1 - chi2.pdf(skew, self.get_df())

        kurt = (self.calculate_g_coeff()['g2'] - self.p * (self.p + 2)) * np.sqrt(
            self.n / (8 * self.p * (self.p + 2)))
        p_kurt = 2 * (norm.pdf(abs(kurt)))
        return skew, p_skew, kurt, p_kurt


m = pd.DataFrame(np.array([2, 3, 5, 6, 3, 2, 5, 5, 2]).reshape((3, 3)))

m_test = Mardia(m, cov=True)
print(m_test.calculate_d())
