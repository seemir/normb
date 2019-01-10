# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from scipy.stats import jarque_bera, normaltest, shapiro, kstest, anderson
from prettytable import PrettyTable
from bisect import bisect_left
import pandas as pd


class NormalityBattery:

    def __init__(self, df):
        """
        Initiate the class

        Parameters
        ----------
        df      : pandas.core.frame.DataFrame
                  Dataframe for which one wants to test for normality

        """
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df)))
        self.df = df

    @staticmethod
    def _astrix(p_value):
        """
        Method for producing correct astrix notation given a p-value

        Parameters
        ----------
        p_value   : float
                    p-value to be looked-up
        Returns
        -------
        Out     : string
                  correct astrix notation

        """
        try:
            p_value = float(p_value)
        except Exception:
            raise TypeError("p_val must be of type 'float', got {}".format(type(p_value)))

        sign_limit = [0.0001, 0.001, 0.01, 0.05, ]
        sign_stars = ['****', '***', '**', '*', '']
        return sign_stars[bisect_left(sign_limit, p_value)]

    def get_dimensions(self):
        """
        Gets the dimensions of the Dataframe initiated

        Returns
        -------
        Out     : tuple
                  dimensions of df

        """
        return self.df.shape

    def check_normality(self, dim='col', digits=5):
        """
        Checks to see if the values in the rows or columns of a dataframe are normally distributed
        using Anderson-Darling, Jarque-Bera, D’Agostino / Pearson’s, Kolmogorov–Smirnov and
        Shapiro-Wilk.

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down

        Returns
        -------
        Out     : prettytable
                  table containing test-statistic and p-value of row/col vectors

        """
        table = PrettyTable()
        rnd, d = round, digits

        dim_name = 'col' if dim == 'col' else 'row'
        table.field_names = [dim_name,
                             'ad', 'p-value (ad)',
                             'jb', 'p-value (jb)',
                             'k2', 'p-value (k2)',
                             'ks', 'p-value (ks)',
                             'sw', 'p-value (sw)']
        vectors = self.df.iteritems() if dim == "col" else self.df.iterrows()

        for i, vector in vectors:
            ad, p_ad = anderson(vector)[0], anderson(vector)[1][2]
            jb, p_jb = jarque_bera(vector)
            k2, p_pr, = normaltest(vector)
            ks, p_ks = kstest(vector, cdf='norm')
            sw, p_sw = shapiro(vector)
            table.add_row([rnd(i + 1, d),
                           rnd(ad, d), "{}{}".format(rnd(p_ad, d), self._astrix(rnd(p_ad, d))),
                           rnd(jb, d), "{}{}".format(rnd(p_jb, d), self._astrix(rnd(p_jb, d))),
                           rnd(k2, d), "{}{}".format(rnd(p_pr, d), self._astrix(rnd(p_pr, d))),
                           rnd(ks, d), "{}{}".format(rnd(p_ks, d), self._astrix(rnd(p_ks, d))),
                           rnd(sw, d), "{}{}".format(rnd(p_sw, d), self._astrix(rnd(p_sw, d)))])
        table.title = 'Normality test of ' + dim_name + ' vectors in DataFrame(df)'
        return table
