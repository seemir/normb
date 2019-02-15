# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects import r
import numpy as np
import pandas as pd


class Royston:

    def __init__(self, df):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  df to be analysed

        """
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df).__name__))
        self.df = numpy2ri(np.array(df, dtype=float))

    def run_royston_test(self):
        """
        Runs the Royston test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('library("MVN")')
        r.assign("df", self.df)
        r('res <- mvn(df, mvnTest = "royston")')

    def print_results(self):
        """
        Gets the Royston test statistic and p-value

        Returns
        -------
        Out     : tuple
                  (hz test statistic, p-value)

        """
        self.run_royston_test()
        roy = r('as.numeric(res$multivariateNormality["H"])')
        p_roy = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(roy) + list(p_roy))