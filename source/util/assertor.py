# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exceptions.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.exceptions.only_numeric_df_accepted import OnlyNumericDfAccepted
import pandas as pd
import numpy as np


class Assertor:
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
                "object must be of type 'pandas.DataFrame', got '{}'".format(type(obj).__name__))

    @staticmethod
    def evaluate_data_type(arg_dict: dict):
        """
        Method that evaluates the type of objects in dictionary of {objects: types}. Raises
        TypeError if not match.

        Parameters
        ----------
        arg_dict    : dict
                      dict of arg: type to be evaluated

        """
        for arg, t in arg_dict.items():
            if not isinstance(arg, t):
                raise TypeError(
                    "expected type '{}', got '{}' instead".format(t.__name__, type(arg).__name__))

    @staticmethod
    def evaluate_numeric_df(df: pd.DataFrame):
        """

        Parameters
        ----------
        df      : pandas.DataFrame
                  DataFrame to be evaluated if is numeric

        """
        if df.shape[1] != df.select_dtypes(include=np.number).shape[1]:
            raise OnlyNumericDfAccepted("only numeric df accepted: got {}".format(type(df)))

    def __init__(self):
        """
        Constructor / Instantiating the class

        """
        if type(self) == Assertor:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))
