#! /usr/bin/env python3
"""brandespich_sample.py

Compute approximations of the betweenness centrality of all the vertices
in the graph using the algorithm by Brandes and Pich, and the time needed to
compute them. These values are then written to an output file. For the
algorithm, see http://www.worldscientific.com/doi/abs/10.1142/S0218127407018403 .

"""
import argparse
import itertools
import logging
import math
import random
import sys
import time

import brandes_exact
import util

def betweenness(graph, epsilon, delta, set_attributes=True):
    """Compute approx. betweenness using Brandes and Pick algorithm.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using the algorithm by Brandes and Pich, and the time needed to
    compute them. For the algorihm, see
    http://www.worldscientific.com/doi/abs/10.1142/S0218127407018403 .

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    # We do not use logging from here to the end of the computation to avoid
    # wasting time
    logging.info("Computing approximate betweenness using Brandes and Pich algorithm")
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_bp(epsilon, delta)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    stats["time"] = elapsed_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    stats["delta"] = delta
    stats["epsilon"] = epsilon
    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["bp_" + key] = stats[key]
        graph.vs["bp_betw"] = betw

    return (stats, betw)

def main():
    """Parse arguments and perform the computation."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute approximate betweenness centrality of all vertices in a graph using the algorihm by Brandes and Pich, and the time to compute them, and write them to file"
    parser.add_argument("epsilon", type=util.valid_interval_float,
            help="accuracy parameter")
    parser.add_argument("delta", type=util.valid_interval_float,
            help="confidence parameter")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the approximate betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # Compute betweenness
    (stats, betw) = betweenness(G, args.epsilon, args.delta, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write stats and betweenness to output
    util.write_to_output(stats, betw, args.output)

if __name__ == "__main__":
    main()

