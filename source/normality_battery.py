# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'
__copyright__ = """
The MIT License (MIT)
Copyright (c) 2019
    Samir Adrik <samir.adrik@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from source.util.descriptive_statistics_generator import DescriptiveStatisticsGenerator
from source.util.multivariate_normality_generator import MultivariateNormalityGenerator
from source.util.univariate_normality_generator import UnivariateNormalityGenerator
from source.util.dataframe_generator import DataFrameGenerator
from source.util.result_generator import ResultGenerator
from pyfiglet import Figlet
from .version import __version__
import numpy as np
import inspect
import datetime
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
        df      : pandas.DataFrame
                  Dataframe for which one wants to test for normality

        """
        DataFrameGenerator.evaluate_pd_dataframe(df)
        DataFrameGenerator.evaluate_numeric_df(df)

        if np.prod(df.shape) < 400:
            raise ValueError(
                "pd.DataFrame must have at least 400 observations, i.e. (20 x 20) in order to "
                "conduct any meaningful normality tests, got {}".format(df.shape))
        self.df = df

    def descriptive_statistics(self, dim='col', digits=5):
        """
        Gets descriptive statistics

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to show descriptive statistics along the columns 'col'
                  or rows 'row', default is 'col'
        digits  : integer
                  number of decimal places to round down

        Returns
        -------
        Out     : str
                  string containing descriptive statistics

        """
        ds = DescriptiveStatisticsGenerator(self.df, dim=dim, digits=digits)
        return ds.generate_descriptive_statistics()

    def univariate_normality(self, dim='col', digits=5):
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
        un = UnivariateNormalityGenerator(self.df, dim=dim, digits=digits)
        return un.generate_univariate_normality_results()

    def multivariate_normality(self, digits=5):
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
        mn = MultivariateNormalityGenerator(self.df, digits=digits)
        return mn.generate_multivariate_normality_results()

    def result_summary(self, dim='col', digits=5):
        """
        Summaries results of statistical tests

        Parameters
        ----------
        dim         : string
                      indicate whether one wants to test for normality along the columns
                      'col' or rows 'row', default is 'col'
        digits      : integer
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

    def normality_report(self, file_dir="reports/txt", dim='col', digits=5, ds=False):
        """
        Method that prints a report containing the results of the Normality tests

        Parameters
        ----------
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

        """
        DataFrameGenerator.evaluate_data_type({file_dir: str, dim: str, digits: int, ds: bool})

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
            file.write('Version: ' + __version__ + '\n')
            file.write(__copyright__)
            file.write(summary + '\n')
            file.write(mn + '\n')
            file.write(un + '\n')
            file.write(self.descriptive_statistics(dim, digits))
        else:
            file.write(title)
            file.write('Version: ' + __version__ + '\n')
            file.write(__copyright__)
            file.write(summary + '\n')
            file.write(self.multivariate_normality(digits) + '\n')
            file.write(self.univariate_normality(dim, digits) + '\n')
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
                method[0] not in ['__init__', 'normality_report', 'results_summary',
                                  '__getmethods__']]
