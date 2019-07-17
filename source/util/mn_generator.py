# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.multivariate_norm.doornik_hansen import DoornikHansen
from source.multivariate_norm.henze_zirkler import HenzeZirkler
from source.util.abstract_generator import AbstractGenerator
from source.multivariate_norm.royston import Royston
from source.multivariate_norm.mardia import Mardia
from source.multivariate_norm.energy import Energy
from prettytable import PrettyTable


class MultivariateNormalityGenerator(AbstractGenerator):
    """
    Class that generates multivariate normality results

    """

    def __init__(self, df, digits=5):
        """
        Constructor / Initiate the class

        Parameters
        ----------
        df      : pandas.DataFrame
                  Dataframe for which one wants to generate / test
        digits  : integer
                  number of decimal places to round down

        """
        super().__init__(digits=digits)
        self.evaluate_pd_dataframe(df)
        self.evaluate_data_type({digits: int})

        self.df = df
        self.digits = digits

    def generate_multivariate_normality_results(self):
        """
        Method that generates multivariate results from a pandas.DataFrame's column or row
        vectors.

        Returns
        -------
        Out     : str
                  String of multivariate results

        """
        self.evaluate_data_type({self.digits: int})

        multi_norm_table = PrettyTable(hrules=3, vrules=2)
        rnd, d = round, self.digits

        multi_norm_header_name = ['', 't1', 'p-value (t1)', 't2', 'p-value (t2)']
        multi_norm_table.field_names = multi_norm_header_name

        # Add Mardia results
        mardia = Mardia(self.df)
        mardia_results = mardia.print_results()
        multi_norm_mardia_row = ['mardia',
                                 rnd(mardia_results[0], d),
                                 self.astrix(rnd(mardia_results[1], d)),
                                 rnd(mardia_results[2], d),
                                 self.astrix(rnd(mardia_results[3], d)),
                                 ]
        multi_norm_table.add_row(multi_norm_mardia_row)

        # Add rest of the results
        methods = {'royston': Royston(self.df),
                   'henze-zirkler': HenzeZirkler(self.df),
                   'doornik-hansen': DoornikHansen(self.df),
                   'energy': Energy(self.df)}

        for name, method in methods.items():
            method_results = method.print_results()
            multi_norm_row = [name,
                              rnd(method_results[0], d),
                              self.astrix(rnd(method_results[1], d)),
                              '', ''
                              ]
            multi_norm_table.add_row(multi_norm_row)

        multi_norm_table.align = "r"

        return str(multi_norm_table)
