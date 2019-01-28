# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from scipy.stats import jarque_bera, normaltest, shapiro, kstest, kurtosis, skew
from numpy import mean, var, std, median, min, max, quantile
from normbatt.df_generator import DataFrameGenerator
from prettytable import PrettyTable
from bisect import bisect_left
import pandas as pd
import os


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
                            ", got {}".format(type(df).__name__))
        self.df = df

    @staticmethod
    def astrix(p_value):
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
        DataFrameGenerator.evaluate_data_type({p_value: float})

        sign_limit = [0.0001, 0.001, 0.01, 0.05, ]
        sign_stars = ['****', '***', '**', '*', '']
        return sign_stars[bisect_left(sign_limit, p_value)]

    def get_dimensions(self):
        """
        Gets the dimensions of the Dataframe initiated

        Returns
        -------
        Out     : string
                  dimensions of df

        """
        return "x".join(str(dim) for dim in self.df.shape)

    def check_univariate_normality(self, dim='col', digits=5, ds=False):
        """
        Checks to see if the values in the rows or columns of a dataframe are univariate normally
        distributed using Jarque-Bera, D’Agostino / Pearson’s, Kolmogorov–Smirnov and Shapiro-Wilk.

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down
        ds      : bool
                  indicating if one wants additional columns with descriptive
                  statistics of the data

        Returns
        -------
        Out     : prettytable
                  table containing test-statistic and p-value of row/col vectors

        """
        DataFrameGenerator.evaluate_data_type({dim: str, digits: int})

        norm_table, desc_table = PrettyTable(vrules=2), PrettyTable(vrules=2)
        rnd, d = round, digits
        dim_name = 'col' if dim == 'col' else 'row'

        if ds:
            decs_header_names = [dim_name,
                                 'mean', 'median',
                                 'variance', 'stdev',
                                 'kurtosis', 'skewness',
                                 'min', 'max',
                                 'quant (95%)']
            desc_table.field_names = decs_header_names

        norm_header_names = [dim_name,
                             'jb', 'p-value (jb)',
                             'k2', 'p-value (k2)',
                             'ks', 'p-value (ks)',
                             'sw', 'p-value (sw)']
        norm_table.field_names = norm_header_names

        vectors = self.df.iteritems() if dim == "col" else self.df.iterrows()
        for i, vector in vectors:
            if ds:
                desc_row = [rnd(i + 1, d),
                            rnd(mean(vector), d), rnd(median(vector), d),
                            rnd(var(vector), d), rnd(std(vector), d),
                            rnd(kurtosis(vector), d), rnd(skew(vector), d),
                            rnd(min(vector), d), rnd(max(vector), d),
                            rnd(quantile(vector, 0.95), d)]
                desc_table.add_row(desc_row)
                desc_table.align = "r"

            jb, p_jb = jarque_bera(vector)
            k2, p_pr, = normaltest(vector)
            ks, p_ks = kstest(vector, cdf='norm')
            sw, p_sw = shapiro(vector)
            norm_row = [rnd(i + 1, d),
                        rnd(jb, d), "{}{}".format(rnd(p_jb, d), self.astrix(rnd(p_jb, d))),
                        rnd(k2, d), "{}{}".format(rnd(p_pr, d), self.astrix(rnd(p_pr, d))),
                        rnd(ks, d), "{}{}".format(rnd(p_ks, d), self.astrix(rnd(p_ks, d))),
                        rnd(sw, d), "{}{}".format(rnd(p_sw, d), self.astrix(rnd(p_sw, d)))]

            norm_table.add_row(norm_row)
            norm_table.align = "r"

        desc_table.title = 'Descriptive statistics ' + self.get_dimensions() + ' DataFrame(df)'
        norm_table.title = 'Normality test ' + self.get_dimensions() + ' DataFrame(df)'

        return list(map(str, [desc_table, norm_table])) if ds else str(norm_table)

    def print_report(self, filename="NormalityReport.txt", file_dir="reports/", dim='col', digits=5,
                     ds=False):
        """
        Method that prints a report containing the results of the Normality tests

        Parameters
        ----------
        filename    : str
                      name of file to be produced
        file_dir    : str
                      directory to save the file
        ds          : bool
                      indicating if one wants additional columns with descriptive
                      statistics of the data
        """
        DataFrameGenerator.evaluate_data_type({filename: str, file_dir: str})

        try:
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        file = open(os.path.join(file_dir, filename), "w")
        if ds:
            file.write(self.check_univariate_normality(dim, digits, ds=ds)[0] + '\n')
            file.write(self.check_univariate_normality(dim, digits, ds=ds)[1])
        else:
            file.write(self.check_univariate_normality(dim, digits, ds=ds))
        file.close()
