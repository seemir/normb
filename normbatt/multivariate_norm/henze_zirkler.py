# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects import r
import numpy as np
import pandas as pd


class HenzeZirkler:

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

    def run_hz_test(self):
        """
        Runs the Henze-Zirkler test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('library("MVN")')
        r.assign("df", self.df)
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