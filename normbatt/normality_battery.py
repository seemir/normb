# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from normbatt.util.pdf_writer import PDFWriter
from normbatt.multi_norm.mardia import Mardia
from normbatt.multi_norm.henze_zirkler import HenzeZirkler
from normbatt.multi_norm.royston import Royston
from prettytable import PrettyTable
from bisect import bisect_left
import scipy.stats as stats
import numpy as np
import pandas as pd
import os


class NormalityBattery:
    """
    Battery of univariate normality tests on row or column vectors of pandas.DataFrame

    """

    def __init__(self, df):
        """
        Constructor / Initiate the class

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

    def print_descriptive_statistics(self, dim='col', digits=5):
        """
        Get string of descriptive statistics

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down

        Returns
        -------
        Out     : str
                  string containing descriptive statistics

        """
        DataFrameGenerator.evaluate_data_type({dim: str, digits: int})

        desc_table = PrettyTable(vrules=2)
        rnd, d = round, digits
        dim_name = 'col' if dim == 'col' else 'row'

        decs_header_names = [dim_name,
                             'mean', 'median',
                             'variance', 'stdev',
                             'kurtosis', 'skewness',
                             'min', 'max',
                             'quant (95%)']
        desc_table.field_names = decs_header_names

        vectors = self.df.iteritems() if dim == "col" else self.df.iterrows()

        for i, vector in vectors:
            desc_row = [rnd(i + 1, d),
                        rnd(np.mean(vector), d), rnd(np.median(vector), d),
                        rnd(np.var(vector), d), rnd(np.std(vector), d),
                        rnd(stats.kurtosis(vector), d), rnd(stats.skew(vector), d),
                        rnd(min(vector), d), rnd(max(vector), d),
                        rnd(np.quantile(vector, 0.95), d)]
            desc_table.add_row(desc_row)
            desc_table.align = "r"

        desc_table.title = 'Descriptive statistics ' + self.get_dimensions() + ' DataFrame(df)'
        return str(desc_table)

    def print_univariate_normality(self, dim='col', digits=5):
        """
        Checks to see if the values in the rows or columns of a dataframe are univariate normally
        distributed using Jarque-Bera, D’Agostino / Pearson’s, Kolmogorov–Smirnov and Shapiro-Wilk.

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down results

        Returns
        -------
        Out     : str
                  string containing test-statistic and p-value of row/col vectors

        """
        DataFrameGenerator.evaluate_data_type({dim: str, digits: int})

        norm_table = PrettyTable(vrules=2)
        rnd, d = round, digits
        dim_name = 'col' if dim == 'col' else 'row'

        norm_header_names = [dim_name,
                             'jb', 'p-value (jb)',
                             'k2', 'p-value (k2)',
                             'ks', 'p-value (ks)',
                             'sw', 'p-value (sw)']
        norm_table.field_names = norm_header_names

        vectors = self.df.iteritems() if dim == "col" else self.df.iterrows()
        for i, vector in vectors:
            jb, p_jb = stats.jarque_bera(vector)
            k2, p_pr, = stats.normaltest(vector)
            ks, p_ks = stats.kstest(vector, cdf='norm')
            sw, p_sw = stats.shapiro(vector)
            norm_row = [rnd(i + 1, d),
                        rnd(jb, d), "{}{}".format(rnd(p_jb, d), self.astrix(rnd(p_jb, d))),
                        rnd(k2, d), "{}{}".format(rnd(p_pr, d), self.astrix(rnd(p_pr, d))),
                        rnd(ks, d), "{}{}".format(rnd(p_ks, d), self.astrix(rnd(p_ks, d))),
                        rnd(sw, d), "{}{}".format(rnd(p_sw, d), self.astrix(rnd(p_sw, d)))]

            norm_table.add_row(norm_row)
            norm_table.align = "r"

        norm_table.title = 'Univariate Normality test ' + self.get_dimensions() + ' DataFrame(df)'
        return str(norm_table)

    def print_multivariate_normality(self, digits=5):
        """
        Check to see if values of numeric DataFrame follows a multivariate normal distribution

        Parameters
        ----------
        digits  : integer
                  number of decimal places to round down results

        Returns
        -------
        Out     : str
                  string containing test-statistic and p-value of row/col vectors

        """
        DataFrameGenerator.evaluate_data_type({digits: int})

        multi_norm_table = PrettyTable(vrules=2)
        rnd, d = round, digits

        multi_norm_header_name = ['', 't1', 'p-value (t1)', 't2', 'p-value (t2)']
        multi_norm_table.field_names = multi_norm_header_name

        mardia = Mardia(self.df)
        hz = HenzeZirkler(self.df)
        roy = Royston(self.df)

        # Add Mardia results
        multi_norm_mardia_row = ['mardia',
                                 rnd(mardia.print_results()[0], d),
                                 rnd(mardia.print_results()[1], d),
                                 rnd(mardia.print_results()[2], d),
                                 rnd(mardia.print_results()[3], d),
                                 ]
        multi_norm_table.add_row(multi_norm_mardia_row)

        # Add Royston results
        multi_norm_roy_row = ['royston',
                              rnd(roy.print_results()[0], d),
                              rnd(roy.print_results()[1], d),
                              '', ''
                              ]
        multi_norm_table.add_row(multi_norm_roy_row)

        # Add HZ results
        multi_norm_hz_row = ['hz',
                             rnd(hz.print_results()[0], d),
                             rnd(hz.print_results()[1], d),
                             '', ''
                             ]
        multi_norm_table.add_row(multi_norm_hz_row)
        multi_norm_table.align = "r"
        multi_norm_table.title = 'Multivariate Normality test ' + self.get_dimensions() + \
                                 ' DataFrame(df)'
        return str(multi_norm_table)

    def print_report(self, file_name="NormalityReport.txt", file_dir="reports/", dim='col',
                     digits=5, ds=False, pdf=False):
        """
        Method that prints a report containing the results of the Normality tests

        Parameters
        ----------
        file_name    : str
                      name of file to be produced
        file_dir    : str
                      directory to save the file
        dim         : string
                      indicate whether one wants to test for normality along the columns
                      'col' or rows 'row', default is 'col'
        digits      : integer
                      number of decimal places to round down
        ds          : bool
                      indicating if one wants additional table with descriptive
                      statistics of the data
        pdf         : bool
                      indicating whether one wants to print report as pdf

        """
        DataFrameGenerator.evaluate_data_type(
            {file_name: str, file_dir: str, dim: str, digits: int, ds: bool, pdf: bool})

        try:
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        file = open(os.path.join(file_dir, file_name), "w")
        if ds:
            file.write(self.print_descriptive_statistics(dim, digits) + '\n')
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
            if pdf:
                pw = PDFWriter(file_name[:-4] + '.pdf', file_dir)
                pw.set_font('Courier', 8.5)
                for line in self.print_descriptive_statistics(dim, digits).split('\n'):
                    pw.write_line(line)
                for line in self.print_multivariate_normality(digits).split('\n'):
                    pw.write_line(line)
                for line in self.print_univariate_normality(dim, digits).split('\n'):
                    pw.write_line(line)
                pw.close()
        else:
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
            if pdf:
                pw = PDFWriter(file_name[:-4] + '.pdf', file_dir)
                pw.set_font('Courier', 8.5)
                for line in self.print_multivariate_normality(digits).split('\n'):
                    pw.write_line(line)
                for line in self.print_univariate_normality(dim, digits).split('\n'):
                    pw.write_line(line)
                pw.close()
        file.close()
