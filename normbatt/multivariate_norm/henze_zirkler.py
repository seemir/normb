# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.multivariate_norm.abstract_normality_test import AbstractNormalityTest
from rpy2.robjects import r


class HenzeZirkler(AbstractNormalityTest):
    """
    Implements the Henze-Zirkler test for multivariate normality

    """

    def __init__(self, df):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  df to be analysed

        """
        super().__init__(df)

    def run_hz_test(self):
        """
        Runs the Henze-Zirkler test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('res <- mvn(df, mvnTest = "hz")')

    def print_results(self):
        """
        Gets the hz test statistic and p-value

        Returns
        -------
        Out     : tuple
                  (hz test statistic, p-value)

        """
        self.run_hz_test()
        hz = r('as.numeric(res$multivariateNormality["HZ"])')
        p_hz = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(hz) + list(p_hz))
