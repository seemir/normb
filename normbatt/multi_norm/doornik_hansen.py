# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects import r
import numpy as np
import pandas as pd


class DoornikHansen:

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

    def run_dh_test(self):
        """
        Runs the Doornik-Hansen test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('library("MVN")')
        r.assign("df", self.df)
        r('res <- mvn(df, mvnTest = "dh")')

    def print_results(self):
        """
        Gets the dh test statistic and p-value

        Returns
        -------
        Out     : tuple
                  (dh test statistic, p-value)

        """

        # TODO: Fix bug, returns nan when data is normally distributed
        self.run_dh_test()
        dh = r('as.numeric(res$multivariateNormality["E"])')
        p_dh = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(dh) + list(p_dh))
