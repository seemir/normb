# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.generator import Generator
from source.util.assertor import Assertor
from prettytable import PrettyTable
import pandas as pd


class ResultGenerator(Generator):
    """
    Class that generates results from all statistical tests

    """

    def __init__(self, df: pd.DataFrame, mn: str, un: str, dim: str = 'col', digits: int = 5):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  DataFrame used for analysis
        mn      : str
                  string with all the results from the multivariate normality tests
        un      : str
                  string with all the results from the univariate normality tests
        dim     : str
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : int
                  number of decimal places to round down

        """
        super().__init__(dim=dim, digits=digits)
        Assertor.evaluate_pd_dataframe(df)
        Assertor.evaluate_numeric_df(df)
        Assertor.evaluate_data_type({mn: str, un: str, dim: str, digits: int})

        self.df = df
        self.mn = mn
        self.un = un
        self.dim = dim
        self.digits = digits

    def generate_result_summary(self):
        """
        Summaries results of statistical tests

        Returns
        -------
        out         : tuple
                      (summary, un, mn-objects)

        """
        rnd, d = round, self.digits

        mn_tot = 6
        mn_pass = self.count_astrix(self.mn)
        mn_fail = mn_tot - mn_pass
        mn_pr, mn_fr = rnd(mn_pass / mn_tot, d), rnd(1 - mn_pass / mn_tot, d)

        un_tot = 4 * self.df.shape[1] if self.dim == 'col' else 4 * self.df.shape[0]
        un_pass = self.count_astrix(self.un)
        un_fail = un_tot - un_pass
        un_pr, un_fr = rnd(un_pass / un_tot, d), rnd(1 - un_pass / un_tot, d)

        tot = mn_tot + un_tot
        passed, failed = mn_pass + un_pass, mn_fail + un_fail
        tot_pr, tot_fr = rnd(passed / tot, d), rnd(failed / tot, d)

        summary = PrettyTable(vrules=2)
        summary.field_names = ['',
                               ' conducted',
                               '  conclusive',
                               '  (c-rate)',
                               'inconclusive',
                               '  (i-rate)'
                               ]

        summary.add_row(['  multivariate', '6', str(mn_pass), str(mn_pr), str(mn_fail), str(mn_fr)])
        summary.add_row(
            ['  univariate', un_tot, str(un_pass), str(un_pr), str(un_fail), str(un_fr)])

        summary.add_row(['', '- - - - -', '- - - - -', '- - - - -', '- - - - -', '- - - - -'])
        summary.add_row(['total', str(tot), str(passed), str(tot_pr), str(failed), str(tot_fr)])
        summary.align = 'r'
        return str(summary), self.mn, self.un
