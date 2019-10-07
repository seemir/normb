# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class OnlyNumericDfAccepted(Exception):
    """
    Exception thrown when Non df is passed

    """

    def __init__(self, msg: str):
        self.msg = msg
