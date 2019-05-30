# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd


class AbstractGenerator:
    """
    Superclass for which all generators are subclassed.

    """

    @staticmethod
    def evaluate_pd_dataframe(obj):
        """
        Method that evaluate if an object is a pandas.Dataframe, raises TypeError if not match

        Parameters
        ----------
        obj     : object
                  object to be evaluated

        """
        if not isinstance(obj, pd.DataFrame):
            raise TypeError(
                "object must be of type 'pandas.DataFrame', got {}".format(type(obj).__name__))

    @staticmethod
    def evaluate_data_type(arg_dict):
        """
        Method that evaluates the type of objects in dictionary of {objects: types}. Raises
        TypeError if not match.

        Parameters
        ----------
        arg_dict    : dictionary
                      dict of arg: type to be evaluated

        """
        for arg, t in arg_dict.items():
            if not isinstance(arg, t):
                raise TypeError(
                    "Expected type '{}', got '{}' instead".format(t.__name__, type(arg).__name__))

    def __init__(self, dim='col', digits=5, seed=90210):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        dim     : string
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : integer
                  number of decimal places to round down
        seed    : int
                  User can set a seed parameter to generate deterministic, non-random output

        """
        if type(self) == AbstractGenerator:
            raise TypeError("base class AbstractGenerator cannot be instantiated")

        self.evaluate_data_type({dim: str, digits: int, seed: int})
        self.dim = dim
        self.digits = digits
        self.seed = seed
