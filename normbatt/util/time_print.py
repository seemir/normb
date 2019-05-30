# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import datetime


def time_progress_print(prefix, method, start):
    """
    Method that print message "prefix (e.g. running, calling, completed etc) method: 'method'() ... elapsed time ()"

    """
    print("{} method: {}() ... elapsed time ({})".format(prefix, method, datetime.datetime.now() - start) + "\n")


def time_print(prefix, method, start):
    """
    Method that print message "prefix (e.g. running, calling, completed etc) method ... (finished at time)

    """
    print("{} {} ... (finished at {})".format(prefix, method, str(start)))
