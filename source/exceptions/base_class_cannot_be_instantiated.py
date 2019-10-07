# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class BaseClassCannotBeInstantiated(Exception):
    """
    Exception thrown when base class is attempted to be instantiated

    """

    def __init__(self, msg: str):
        self.msg = msg
