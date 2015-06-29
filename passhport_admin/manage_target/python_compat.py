# -*-coding:Utf-8 -*-

"""Contains compatibility’s functions (version 2.7)"""


def input_compat(arg):
    """Defines input as raw_input for compatibility with 2.7 version"""
    try:
        input = raw_input
    except NameError:
        pass

    return input(arg)
