"""util.py

Various useful functions.
"""
import argparse
import logging
import sys
import igraph as ig

def read_graph(path):
    """Read an igraph.Graph from the file path. Return graph."""
    logging.info("Reading graph from %s", path) 
    try:
        G = ig.Graph.Read(path)
    except OSError as E:
        # XXX There seems to be some problem in the propagation of E.strerror,
        # so the following actually print None at the end. Not our fault. We
        # leave it here as perhaps it will be fixed upstream at some point.
        logging.critical("Cannot read graph file %s: %s", E.strerror)
        sys.exit(2)
    return G

def set_verbosity(level):
     """Set the desired level of logging."""

     log_format='%(levelname)s: %(message)s'
     if level == 1:
         logging.basicConfig(format=log_format, level=logging.INFO)
     elif level >= 2:
         logging.basicConfig(format=log_format, level=logging.DEBUG)

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

