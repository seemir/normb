# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.ds_generator import DescriptiveStatisticsGenerator
from source.util.mn_generator import MultivariateNormalityGenerator
from source.util.un_generator import UnivariateNormalityGenerator
from source.util.df_generator import DataFrameGenerator
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
        if np.prod(df.shape) < 8:
            raise ValueError(
                "pd.DataFrame must have more that 8 observations inorder to conduct any "
                "normality test, got {}".format(df.count()))
        self.df = df

    def print_descriptive_statistics(self, dim='col', digits=5):
        """
        Get string of descriptive statistics

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
        un = UnivariateNormalityGenerator(self.df, dim=dim, digits=digits)
        return un.generate_univariate_normality_results()

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
        mn = MultivariateNormalityGenerator(self.df, digits=digits)
        return mn.generate_multivariate_normality_results()

    def print_report(self, file_dir="reports/txt", dim='col', digits=5, ds=False):
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
        if ds:
            file.write(self.print_descriptive_statistics(dim, digits) + '\n')
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
        else:
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
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
                method[0] not in ['__init__', 'print_report', '__getmethods__']]
