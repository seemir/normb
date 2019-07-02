# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.df_generator import DataFrameGenerator
from rpy2.robjects import r, numpy2ri
import numpy as np
import gc


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
            raise TypeError("base class cannot be instantiated")

        DataFrameGenerator.evaluate_pd_dataframe(df)
        r('if (!is.element("MVN", installed.packages()[,1])){ '
          'install.packages("MVN", dep = TRUE)}')
        self.df = numpy2ri.numpy2ri(np.array(df))
        gc.collect()
