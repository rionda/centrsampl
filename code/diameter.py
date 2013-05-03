#! /usr/bin/env python3
"""diameter.py

Compute the diameter of a graph and the time needed to compute it, and write
these info as graph attributes.

"""
import argparse
import logging
import time

import util

def main():  
    """Parse arguments, perform the computation, write to file."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the diameter of a graph and the time needed to compute it, and (if specified) write these info as a graph attributes"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
    help="write the diameter of the graph as the 'diameter' graph attribute and the time taken to compute it as the 'diam_time' attribute")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph from file
    G = util.read_graph(args.graph)

    # Compute the diameter
    logging.info("Computing diameter")
    # time.process_time() does not account for sleeping time. Seems the right
    # function to use. Alternative could be time.perf_counter()
    start_time = time.process_time()
    # XXX What exactly does this compute? Especially for directed graphs
    diameter = G.diameter() # This is not the vertex-diameter !!! 
    end_time = time.process_time()
    elapsed_time = end_time - start_time

    # Print info
    logging.info("Diameter is %d, computed in %f seconds", diameter,
            elapsed_time)
    print("{}, diameter={}, time={}".format(args.graph, diameter,
        elapsed_time))

    # If requested, add graph attributes and write graph back to original file
    if args.write:
        logging.info("Writing diameter and time to graph")
        G["diam"] = diameter
        G["diam_time"] = elapsed_time
        # We use format auto-detection, which should work given that it worked
        # when we read the file
        G.write(args.graph) 

if __name__ == "__main__":
    main()

