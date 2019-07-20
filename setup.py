# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from distutils.core import setup
import sys


def get_version():
    sys.path.insert(0, 'pyfiglet')
    from source.version import __version__
    sys.path.pop(0)
    return __version__


setup(
    name='normb',
    version=get_version(),
    packages=['tests', 'source', 'source.util', 'source.multivariate_norm', 'source.exceptions'],
    requires=['numpy (>=1.15.4)', 'pandas (>=0.24.0)', 'PrettyTable (>=0.7.2)',
              'pytest (>=4.0.2)', 'rpy2 (>=2.9.4)', 'scipy (>=1.2.1)'],
    url='',
    license='MIT',
    author='samir',
    author_email='samir.adrik@gmail.com',
    description='Battery of normality tests for numeric pandas.DataFrame'
)
