# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.multivariate_norm.normality_test import NormalityTest
from rpy2.robjects import r
import pandas as pd
import gc


class DoornikHansen(NormalityTest):
    """
    Implementation of the Doornik-Hansen test for multivariate normality

    """

    def __init__(self, df: pd.DataFrame):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  df to be analysed

        """
        super().__init__(df)

    def run_dh_test(self):
        """
        Runs the Doornik-Hansen test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('require("MVN", character.only = TRUE)')
        r.assign("df", self.df)
        r('res <- mvn(df, mvnTest = "dh")')
        gc.collect()

    def print_results(self):
        """
        Gets the dh test statistic and p-value

        Returns
        -------
        Out     : tuple
                  (dh test statistic, p-value)

        """
        self.run_dh_test()
        dh = r('as.numeric(res$multivariateNormality["E"])')
        p_dh = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(dh) + list(p_dh))
