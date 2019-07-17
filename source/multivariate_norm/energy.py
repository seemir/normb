# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.multivariate_norm.abstract_normality_test import AbstractNormalityTest
from rpy2.robjects import r
import gc


class Energy(AbstractNormalityTest):
    """
    Implements the the Energy E test for multivariate normality
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

    def run_e_test(self, boot=100):
        """
        Runs the Energy E test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('require("MVN", character.only = TRUE)')
        r.assign("df", self.df)
        r('res <- mvn(df, mvnTest = "energy", R = {})'.format(boot))
        gc.collect()

    def print_results(self):
        """
        Gets the dh test statistic and p-value
        Returns
        -------
        Out     : tuple
                  (e test statistic, p-value)

        """
        self.run_e_test()
        dh = r('as.numeric(res$multivariateNormality[2])')
        p_dh = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(dh) + list(p_dh))
