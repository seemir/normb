# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exceptions.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.assertor import Assertor
from bisect import bisect_left
import inspect


class Generator:
    """
    Superclass for which all generators are subclassed.

    """

    @staticmethod
    def astrix(p_value: float):
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
        Assertor.evaluate_data_type({p_value: float})

        sign_limit = [0.0001, 0.001, 0.01, 0.05, ]
        sign_stars = ['****', '***', '**', '*', '']
        return "{}{}".format(p_value, sign_stars[bisect_left(sign_limit, p_value)])

    @staticmethod
    def count_astrix(string: str):
        """
        Count the number of statistical tests that passed based on the astrix notation

        Parameters
        ----------
        string  : str
                  string with results

        Returns
        -------
        Out     : int
                  number of statistical tests that have passed

        """
        Assertor.evaluate_data_type({string: str})

        count = 0
        temp = []
        for char in string + ' ':
            if char != '*':
                if not temp:
                    continue
                else:
                    count += 1
                    temp = []
            else:
                temp.append(char)
        return count

    def __init__(self, dim: str = 'col', digits: int = 5, seed: int = 90210,
                 size: (tuple, int) = (30, 30)):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        dim     : str
                  indicate whether one wants to test for normality along the columns 'col' or rows
                  'row', default is 'col'
        digits  : int
                  number of decimal places to round down
        seed    : int
                  User can set a seed parameter to generate deterministic, non-random output
        size    : tuple of integers, integer
                  dimensions or range of numbers in generated df, default is (30, 30)

        """
        if type(self) == Generator:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))

        if any(dim < 0 for dim in size):
            raise ValueError("dimensions in size cannot be negative")

        Assertor.evaluate_data_type({dim: str, digits: int, seed: int})
        self.dim = dim
        self.digits = digits
        self.seed = seed
        self.size = size

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
