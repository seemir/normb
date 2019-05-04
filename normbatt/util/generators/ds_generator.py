# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.util.generators.abstract_generator import AbstractGenerator
from prettytable import PrettyTable
import scipy.stats as stats
import pandas as pd
import numpy as np


class DsGenerator(AbstractGenerator):

    def __init__(self, df, dim, digits):
        try:
            df = pd.DataFrame(df)
        except Exception:
            raise TypeError("df must be of type 'pandas.core.frame.DataFrame'"
                            ", got {}".format(type(df).__name__))

        super().__init__(dim, digits)
        self.evaluate_data_type({dim: str, digits: int})

        self.df = df
        self.dim = dim
        self.digits = digits

    def generate_desciptive_statistics(self):
        desc_table = PrettyTable(vrules=2)
        rnd, d = round, self.digits
        dim_name = 'col' if self.dim == 'col' else 'row'

        decs_header_names = [dim_name,
                             'mean', 'median',
                             'variance', 'stdev',
                             'kurtosis', 'skewness',
                             'min', 'max',
                             'quant (95%)']
        desc_table.field_names = decs_header_names

        vectors = self.df.iteritems() if self.dim == "col" else self.df.iterrows()

        for i, vector in vectors:
            desc_row = [rnd(i + 1, d),
                        rnd(np.mean(vector), d), rnd(np.median(vector), d),
                        rnd(np.var(vector), d), rnd(np.std(vector), d),
                        rnd(stats.kurtosis(vector), d), rnd(stats.skew(vector), d),
                        rnd(min(vector), d), rnd(max(vector), d),
                        rnd(np.quantile(vector, 0.95), d)]
            desc_table.add_row(desc_row)
            desc_table.align = "r"

        desc_table.title = 'Descriptive statistics ' + self.get_dimensions() + ' DataFrame(df)'
        return str(desc_table)
