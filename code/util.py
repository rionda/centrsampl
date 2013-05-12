"""util.py

Various useful functions.
"""
import argparse
import logging
import pickle
import sys
import igraph as ig

def dict_to_csv(dictionary, csvkeys):
    """Returns a string of comma separated values from a dictionary.
    
    cvskeys is a string of comma separated (potential) keys to be considered.

    """
    keys = map(lambda x: x.strip(), csvkeys.split(","))
    return ", ".join([dict_value_to_str(dictionary, key) for key in keys])

def dict_value_to_str(dictionary, key):
    """Convert value in a dictionary to string.
    
    If dictionary has a key "key", returns the string representation of
    dictionary[key], otherwise returns the empty string.

    """
    string = ""
    if key in dictionary:
        string = str(dictionary[key])
    return string

def positive_int(string):
    """Check validity of string as positive integer. Return value if it is.
    
    To be used as the value for "type" argument in argparse.add_argument().
    If string is valid, return int value of the string. Otherwise raise an
    argparse Error.

    """
    try:
        value = int(string)
        if value < 1:
            msg = "{} is not positive".format(string)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
           msg = "{} is not a valid int".format(string) 
           raise argparse.ArgumentTypeError(msg)
    return value

def read_graph(path):
    """Read an igraph.Graph from the file path. Return graph."""
    logging.info("Reading graph from %s", path) 
    try:
        G = ig.Graph.Read(path)
    except OSError as E:
        # XXX There seems to be some problem in the propagation of E.strerror,
        # so the following actually print None at the end. Not our fault. We
        # leave it here as perhaps it will be fixed upstream at some point.
        logging.critical("Cannot read graph file %s: %s", path, E.strerror)
        sys.exit(2)
    return G

def read_stats_betw(path):
    """Read tuple from pickle file."""
    (stats,betw) = pickle.load(path)
    return (stats,betw)

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

def write_to_output(stats, betw, output_path):
    """ Write stats and betweenness to output file."""
    try:
        with open(output_path, 'wb') as output:
            logging.info("Writing stats and betweenness to output file")
            pickle.dump((stats,betw), output);
            #output.write("({}, {})\n".format(stats, betw))
    except OSError as E:
        logging.critical("Cannot write stats and betweenness to %s: %s", output_path,
                E.strerror)


