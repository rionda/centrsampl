#! /usr/bin/env python3
"""converter.py

Convert an edge list file to an igraph graph and write it to file in pickle
format. The edge list file contains one edge per line as
'from_vertex\tto_vertex'. Lines starting with '#' are treated as comments.  

The graph is simplified if needed (loops and multiple edges are removed).

"""
import argparse
import logging
import os
import os.path
import sys
import igraph as ig

import util

def convert(input_path, is_directed):
    """Convert an edge list file to an igraph.Graph."""

    try: # Handle OSError
        with open(input_path, 'rt') as input_file:
            logging.info("Conversion started")
            if is_directed:
                logging.debug("Considering graph as directed")
            else:
                logging.debug("Considering graph as undirected")
            prev_tell = input_file.tell()
            line = input_file.readline()
            # Skip comments
            while line[0] == "#":
                prev_tell = input_file.tell()
                line = input_file.readline()
            input_file.seek(prev_tell)
            G = ig.Graph.Read_Edgelist(input_file, directed=is_directed)
    except OSError as E:
        logging.critical("Cannot read input file %s: %s", input_path,
                os.strerror(E.errno))
        sys.exit(2)

    logging.info("Conversion complete: %d vertices, %d edges", G.vcount(), G.ecount())

    if not G.is_simple():
        logging.warning("The graph is not simple. We are going to simplify it")
        G.simplify()

    if not G.is_connected(mode=ig.WEAK):
        logging.warning("The graph is not weakly connected. Exiting.")
        exit(2)

    return G

def main():
    """Parse arguments, call convert, write to file."""
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.description = "Convert an edge list file to an igraph graph and write it to file in pickle format. The edge list file contains one edge per line as 'from_vertex\tto_vertex'. Lines at the beginning of the file starting with '#' are treated as comments."
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file (pickle format)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--directed", action="store_true", default=False,
            help="consider the graph as directed")
    group.add_argument("-u", "--undirected", action="store_true", default=True,
            help="consider the graph as undirected (default)")
    parser.add_argument("-v", "--verbose", action="count", default=0,
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-z", "--compress", action="store_true", default=False,
            help="compress the output file")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Convert the file
    G = convert(args.input, args.directed)

    # Serialize the graph to file
    logging.info("Writing graph to file %s", args.output)
    if args.compress:
        logging.debug("Compression selected")
        format = "picklez"
    else:
        format = "pickle"
    G.write(args.output, format)

if __name__ == "__main__":
    main()

