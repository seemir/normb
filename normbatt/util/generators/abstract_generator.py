# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class AbstractGenerator:
    """
    Superclass for which all generators are subclassed.

    """

    @staticmethod
    def evaluate_data_type(arg_dict):
        """
        Method that evaluates the type of an object. Raises TypeError if not match.

        Parameters
        ----------
        arg_dict    : dictionary
                      dict of arg: type to be evaluated

        """
        for arg, t in arg_dict.items():
            try:
                if arg is not None:
                    arg = t(arg)
            except Exception:
                raise TypeError(
                    "Expected type '{}', got '{}' instead".format(t.__name__, type(arg).__name__))

    def __init__(self, dim='col', digits=5, seed=None):
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
        self.evaluate_data_type({dim: str, digits: int, seed: int})
        self.dim = dim
        self.digits = digits
        self.seed = seed

    def get_dimensions(self):
        """
        Gets the dimensions of the Dataframe initiated

        Returns
        -------
        Out     : string
                  dimensions of df

        """
        return "x".join(str(dim) for dim in self.df.shape)
