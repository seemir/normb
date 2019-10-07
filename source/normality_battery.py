# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.descriptive_statistics import DescriptiveStatistics
from source.util.multivariate_normality import MultivariateNormality
from source.util.univariate_normality import UnivariateNormality
from source.util.result_generator import ResultGenerator
from source.util.assertor import Assertor
from pyfiglet import Figlet
from .version import __version__
import pandas as pd
import numpy as np
import inspect
import datetime
import os


class NormalityBattery:
    """
    Battery of univariate normality tests on row or column vectors of pandas.DataFrame

    """

    def __init__(self, df: pd.DataFrame):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  Dataframe for which one wants to test for normality

        """
        Assertor.evaluate_pd_dataframe(df)
        Assertor.evaluate_numeric_df(df)

        if np.prod(df.shape) < 400:
            raise ValueError(
                "pd.DataFrame must have at least 400 observations, i.e. (20 x 20) in order to "
                "conduct any meaningful normality tests, got {}".format(df.shape))
        self.df = df

    def descriptive_statistics(self, dim: str = 'col', digits: int = 5):
        """
        Gets descriptive statistics

        Parameters
        ----------
        dim     : str
                  indicate whether one wants to show descriptive statistics along the columns 'col'
                  or rows 'row', default is 'col'
        digits  : int
                  number of decimal places to round down

        Returns
        -------
        Out     : str
                  string containing descriptive statistics

        """
        ds = DescriptiveStatistics(self.df, dim=dim, digits=digits)
        return ds.generate_descriptive_statistics()

    def univariate_normality(self, dim: str = 'col', digits: int = 5):
        """
        Checks to see if the values in the rows or columns of a dataframe are univariate normally
        distributed using Jarque-Bera, D’Agostino / Pearson’s, Kolmogorov–Smirnov and Shapiro-Wilk.

        Parameters
        ----------
        dim     : str
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : int
                  number of decimal places to round down results

        Returns
        -------
        Out     : str
                  string containing test-statistic and p-value of row/col vectors

        """
        un = UnivariateNormality(self.df, dim=dim, digits=digits)
        return un.generate_univariate_normality_results()

    def multivariate_normality(self, digits: int = 5):
        """
        Check to see if values of numeric DataFrame follows a multivariate normal distribution

        Parameters
        ----------
        digits  : int
                  number of decimal places to round down results

        Returns
        -------
        Out     : str
                  string containing test-statistic and p-value of row/col vectors

        """
        mn = MultivariateNormality(self.df, digits=digits)
        return mn.generate_multivariate_normality_results()

    def result_summary(self, dim: str = 'col', digits: int = 5):
        """
        Summaries results of statistical tests

        Parameters
        ----------
        dim         : str
                      indicate whether one wants to test for normality along the columns
                      'col' or rows 'row', default is 'col'
        digits      : int
                      number of decimal places to round down

        Returns
        -------
        out         : tuple
                      (summary, un, mn-objects)

        """

        mn = self.multivariate_normality(digits)
        un = self.univariate_normality(dim, digits)
        result_summary = ResultGenerator(self.df, mn, un, dim, digits)
        return result_summary.generate_result_summary()

    def normality_report(self, file_dir: str = "reports/txt", dim: str = 'col', digits: int = 5,
                         ds: bool = False):
        """
        Method that prints a report containing the results of the Normality tests

        Parameters
        ----------
        file_dir    : str
                      directory to save the file
        dim         : str
                      indicate whether one wants to test for normality along the columns
                      'col' or rows 'row', default is 'col'
        digits      : int
                      number of decimal places to round down
        ds          : bool
                      indicating if one wants additional table with descriptive
                      statistics of the data

        """
        Assertor.evaluate_data_type({file_dir: str, dim: str, digits: int, ds: bool})

        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file = open(os.path.join(file_dir, "NormalityReport_" + local_time + ".txt"), "w")
        summary, mn, un = self.result_summary(dim=dim, digits=digits)
        figlet = Figlet(font="slant")
        title = figlet.renderText("normb")

        if ds:
            file.write(title)
            file.write('Version: ' + __version__ + '\n''\n')
            file.write(summary + '\n')
            file.write(mn + '\n')
            file.write(un + '\n')
            file.write(self.descriptive_statistics(dim, digits))
        else:
            file.write(title)
            file.write('Version: ' + __version__ + '\n''\n')
            file.write(summary + '\n')
            file.write(mn + '\n')
            file.write(un + '\n')
        file.close()

    def __getmethods__(self):
        """
        List all methods in class as str


        Returns
        -------
        Out     : list of str
                  names of all methods in class

        """
        return [method[0] for method in inspect.getmembers(self, predicate=inspect.ismethod) if
                method[0] not in ['__init__', 'normality_report', 'result_summary',
                                  '__getmethods__']]
