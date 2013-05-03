"""util.py

Various useful functions.
"""
import argparse

def valid_interval_float(string):
    """Check validity of string as float between 0 and 1 (extremes excluded).
    
    To be used as the value for "type" argument in argparse.add_argument().
    If string is valid, return float value of the string. Otherwise raise an
    argparse Error.

    """
    try:
        value = float(string)
        if value <= 0 or value >= 1:
            msg = "{} is not between 0 and 1 (extremes excluded)".format(string)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
           msg = "{} is not a valid float".format(string) 
           raise argparse.ArgumentTypeError(msg)
    return value



