# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.abstract_generator import AbstractGenerator
from normbatt.multivariate_norm.mardia import Mardia
from normbatt.multivariate_norm.henze_zirkler import HenzeZirkler
from normbatt.multivariate_norm.royston import Royston
from normbatt.multivariate_norm.doornik_hansen import DoornikHansen
from normbatt.multivariate_norm.energy import Energy
from prettytable import PrettyTable
import pandas as pd


class MultivariateNormalityGenerator(AbstractGenerator):
    """
    Class that generates multivariate normality results

    """

    def __init__(self, df, digits):
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

        multi_norm_table = PrettyTable(vrules=2)
        rnd, d = round, self.digits

        multi_norm_header_name = ['', 't1', 'p-value (t1)', 't2', 'p-value (t2)']
        multi_norm_table.field_names = multi_norm_header_name

        mardia = Mardia(self.df)
        roys = Royston(self.df)
        hen_zir = HenzeZirkler(self.df)
        door_hans = DoornikHansen(self.df)
        energy = Energy(self.df)

        # Add Mardia results
        multi_norm_mardia_row = ['mardia',
                                 rnd(mardia.print_results()[0], d),
                                 rnd(mardia.print_results()[1], d),
                                 rnd(mardia.print_results()[2], d),
                                 rnd(mardia.print_results()[3], d),
                                 ]
        multi_norm_table.add_row(multi_norm_mardia_row)

        # Add Royston results
        multi_norm_roy_row = ['royston',
                              rnd(roys.print_results()[0], d),
                              rnd(roys.print_results()[1], d),
                              '', ''
                              ]
        multi_norm_table.add_row(multi_norm_roy_row)

        # Add HZ results
        multi_norm_hz_row = ['henze-zirkler',
                             rnd(hen_zir.print_results()[0], d),
                             rnd(hen_zir.print_results()[1], d),
                             '', ''
                             ]
        multi_norm_table.add_row(multi_norm_hz_row)

        # Add DH results
        multi_norm_dh_row = ['doornik-hansen',
                             rnd(door_hans.print_results()[0], d),
                             rnd(door_hans.print_results()[1], d),
                             '', ''
                             ]
        multi_norm_table.add_row(multi_norm_dh_row)

        # Add E statistic results
        multi_norm_e_row = ['energy',
                            rnd(energy.print_results()[0], d),
                            rnd(energy.print_results()[1], d),
                            '', ''
                            ]
        multi_norm_table.add_row(multi_norm_e_row)

        multi_norm_table.align = "r"
        multi_norm_table.title = 'Multivariate Normality test ' + self.get_dimensions() + \
                                 ' DataFrame(df)'
        return str(multi_norm_table)
