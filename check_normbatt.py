# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from normbatt.df_generator import DataFrameGenerator
from normbatt.normality_battery import NormalityBattery
from normbatt.pdf_writer import PDFWriter

if __name__ == '__main__':
    seed = 90210
    ini_df = DataFrameGenerator(seed)
    results = NormalityBattery(ini_df.normal_data_frame())
    lines = results.check_univariate_normality()

    pw = PDFWriter('test.pdf')
    pw.setFont('Courier', 12)
    pw.setHeader('Demo of PrettyTable to PDF')
    pw.setFooter('Demo of PrettyTable to PDF')
    for line in lines.split('\n'):
        pw.writeLine(line)
    pw.close()

