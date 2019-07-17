# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exceptions.base_class_exception import BaseClassCannotBeInstantiated
from bisect import bisect_left
import pandas as pd
import inspect


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

    def __init__(self, dim='col', digits=5, seed=90210, sample=(30, 30)):
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
        sample  : tuple of integers, integer
                  dimensions or range of numbers in generated df, default is (30, 30)

        """
        if type(self) == AbstractGenerator:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))

        if any(dim < 0 for dim in sample):
            raise ValueError("dimensions in sample cannot be negative")

        self.evaluate_data_type({dim: str, digits: int, seed: int})
        self.dim = dim
        self.digits = digits
        self.seed = seed
        self.sample = sample

    def astrix(self, p_value):
        """
        Method for producing correct astrix notation given a p-value

        Parameters
        ----------
        p_value   : float
                    p-value to be looked-up
        Returns
        -------
        Out     : string
                  correct astrix notation

        """
        self.evaluate_data_type({p_value: float})

        sign_limit = [0.0001, 0.001, 0.01, 0.05, ]
        sign_stars = ['****', '***', '**', '*', '']
        return "{}{}".format(p_value, sign_stars[bisect_left(sign_limit, p_value)])

    def __getmethods__(self):
        """
        List all df methods in class as str

        Returns
        -------
        Out     : list of str
                  names of all methods in class

        """
        return [method[0] for method in inspect.getmembers(self, predicate=inspect.ismethod) if
                method[0] not in ['__init__', '__getmethods__', 'to_excel', 'astrix']]
