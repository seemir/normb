# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects import r
import numpy as np
import pandas as pd


class AbstractNormalityTest:
    """
    Superclass for which all normality tests are subclassed.

    """

    def __init__(self, df):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  df to be analysed

        """
        if type(self) == AbstractNormalityTest:
            raise Exception("base class cannot be instantiated")

        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError(
                "df must be of type 'pandas.DataFrame', got {}".format(type(df).__name__))

        self.df = numpy2ri(np.array(df, dtype=float))
        r('library("MVN")')
        r.assign("df", self.df)
