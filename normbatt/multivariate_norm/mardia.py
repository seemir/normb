# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.multivariate_norm.abstract_normality_test import AbstractNormalityTest
from rpy2.robjects import r


class Mardia(AbstractNormalityTest):
    """
    Implements the Mardia test for multivariate normality

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

    def run_mardia_test(self):
        """
        Runs the Mardia test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('res <- mvn(df, mvnTest = "mardia")')

    def print_results(self):
        """
        Gets the mardia test statistics and p-values

        Returns
        -------
        Out     : tuple
                  (mardia_skew test statistic, p-value,
                   mardia_kurt test statistic, p-value)

        """
        self.run_mardia_test()
        m_skew = r('as.numeric(as.vector(res$multivariateNormality[1, "Statistic"]))')
        p_skew = r('as.numeric(as.vector(res$multivariateNormality[1, "p value"]))')
        m_kurt = r('as.numeric(as.vector(res$multivariateNormality[2, "Statistic"]))')
        p_kurt = r('as.numeric(as.vector(res$multivariateNormality[2, "p value"]))')
        return tuple(list(m_skew) + list(p_skew) + list(m_kurt) + list(p_kurt))
