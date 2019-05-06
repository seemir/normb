# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.ds_generator import DescriptiveStatisticsGenerator
from normbatt.util.generators.mn_generator import MultivariateNormalityGenerator
from normbatt.util.generators.un_generator import UnivariateNormalityGenerator
from normbatt.util.generators.df_generator import DataFrameGenerator
import pandas as pd
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
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df).__name__))
        self.df = df

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

    def print_report(self, file_name="NormalityReport", file_dir="reports/", dim='col',
                     digits=5, ds=False):
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

        """
        DataFrameGenerator.evaluate_data_type(
            {file_name: str, file_dir: str, dim: str, digits: int, ds: bool})

        try:
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file = open(os.path.join(file_dir, file_name + "_" + local_time + ".txt"), "w")
        if ds:
            file.write(self.print_descriptive_statistics(dim, digits) + '\n')
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
        else:
            file.write(self.print_multivariate_normality(digits) + '\n')
            file.write(self.print_univariate_normality(dim, digits))
        file.close()
