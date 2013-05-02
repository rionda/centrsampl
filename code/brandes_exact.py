#! /bin/env python3

import argparse
import logging
import os
import time
import igraph as ig

def main():
    """Compute the exact betweenness centrality of all vertices in a graph using
    Brandes' algorithm and write it to a file. Also compute the time needed to
    compute the betweenness.

    For Brandes' algorithm see
    http://www.tandfonline.com/doi/abs/10.1080/0022250X.2001.9990249
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the exact betweenness centrality of all vertices in a graph using Brandes' algorithm, and the time to compute them, and write them to file"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")
    args = parser.parse_args()

    # Set the desired level of logging
    log_format='%(levelname)s: %(message)s'
    if args.verbose == 1:
        logging.basicConfig(format=log_format, level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(format=log_format, level=logging.DEBUG)

    # Read graph
    logging.info("Reading graph from %s", args.graph)
    G = ig.Graph.Read(args.graph)

    # Compute betweenness
    logging.info("Computing betweenness")
    start_time = time.process_time()
    # XXX TODO Check whether multiple shortest paths are handled correctly!
    betweenness = G.betweenness()
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computed in %s seconds", elapsed_time)

    # If specified write
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.vs["betw"] = betweenness
        G["betw_time"] = elapsed_time
        G.write(args.graph)

    # Write betweenness and time to output
    try:
        with open(args.output, 'wt') as output:
            logging.info("Writing betweenness and time to output file")
            output.write("({}, {})\n".format(betweenness, elapsed_time))
    except OSError as E:
        logging.critical("Cannot write betweenness to %s: %s", args.output,
                os.strerror(E.errno))

if __name__ == "__main__":
    main()

