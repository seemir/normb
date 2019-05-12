# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from distutils.core import setup

setup(
    name='normb',
    version='',
    packages=['tests', 'normbatt', 'normbatt.util', 'normbatt.multivariate_norm'],
    requires=['numpy (>= 1.15.4)', 'pytest (>= 4.0.2)', 'pandas (>= 0.24.0)'],
    url='',
    license='MIT',
    author='samir',
    author_email='samir.adrik@gmail.com',
    description='Battery of normality tests for numeric pandas.DataFrame'
)
