# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.abstract_generator import AbstractGenerator
from prettytable import PrettyTable
import scipy.stats as stats


class UnivariateNormalityGenerator(AbstractGenerator):
    """
    Class that generates univariate normality results

    """

    def __init__(self, df, dim='col', digits=5):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  Dataframe for which one wants to generate / test
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down

        """
        super().__init__(dim=dim, digits=digits)
        self.evaluate_pd_dataframe(df)
        self.evaluate_data_type({dim: str, digits: int})

        self.df = df
        self.dim = dim
        self.digits = digits

    def generate_univariate_normality_results(self):
        """
        Method that generates univariate normality results from a pandas.DataFrame's column or row
        vectors.

        Returns
        -------
        Out     : str
                  String of univariate normality results

        """
        unorm_table = PrettyTable(vrules=2)
        rnd, d = round, self.digits
        dim_name = 'col' if self.dim == 'col' else 'row'

        norm_header_names = ['        ',
                             dim_name,
                             '        jb', 'p-value (jb)',
                             '        k2', 'p-value (k2)',
                             '        ks', 'p-value (ks)',
                             '        sw', 'p-value (sw)']
        unorm_table.field_names = norm_header_names

        vectors = self.df.iteritems() if self.dim == "col" else self.df.iterrows()
        for i, vector in vectors:
            jb, p_jb = stats.jarque_bera(vector)
            k2, p_pr, = stats.normaltest(vector)
            ks, p_ks = stats.kstest(vector, cdf='norm')
            sw, p_sw = stats.shapiro(vector)
            norm_row = ['', rnd(i + 1, d),
                        rnd(jb, d), self.astrix(rnd(p_jb, d)),
                        rnd(k2, d), self.astrix(rnd(p_pr, d)),
                        rnd(ks, d), self.astrix(rnd(p_ks, d)),
                        rnd(sw, d), self.astrix(rnd(p_sw, d))]

            unorm_table.add_row(norm_row)
        unorm_table.align = "r"
        return str(unorm_table)
