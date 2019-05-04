# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects import r
import numpy as np
import pandas as pd


class Energy:

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

    def run_e_test(self):
        """
        Runs the Energy E test for multivariate normality by delegating the task to the
        MVN module in r

        """
        r('library("MVN")')
        r.assign("df", self.df)
        r('res <- mvn(df, mvnTest = "energy")')

    def print_results(self):
        """
        Gets the dh test statistic and p-value

        Returns
        -------
        Out     : tuple
                  (e test statistic, p-value)

        """

        # TODO: Fix bug, returns nan when data is normally distributed
        self.run_e_test()
        dh = r('as.numeric(res$multivariateNormality[2])')
        p_dh = r('as.numeric(res$multivariateNormality["p value"])')
        return tuple(list(dh) + list(p_dh))