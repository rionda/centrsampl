#! /bin/env python3

import argparse
import logging
import time
import igraph as ig

def main():
    """Compute the diameter of the graph and the time needed to compute it, and
    write these info as  graph attributes.
    
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the diameter of a graph and the time needed to compute it, and (if specified) write these info as a graph attributes"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
    help="write the diameter of the graph as the 'diameter' graph attribute and the time taken to compute it as the 'diam_time' attribute")
    args = parser.parse_args()

    # Set the desired level of logging
    log_format='%(levelname)s: %(message)s'
    if args.verbose == 1:
        logging.basicConfig(format=log_format, level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(format=log_format, level=logging.DEBUG)

    # Read graph from file, using auto-detection of format
    logging.info("Reading graph from %s", args.graph) 
    G = ig.Graph.Read(args.graph)

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
        G["diameter"] = diameter
        G["diam_time"] = elapsed_time
        # We use format auto-detection, which should work given that it worked
        # when we read the file
        G.write(args.graph) 

if __name__ == "__main__":
    main()
