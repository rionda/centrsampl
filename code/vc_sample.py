#! /usr/bin/env python3
"""vc_sample.py

Compute approximations of the betweenness centrality of all the vertices in
the graph using random sampling and the VC-dimension, and the time needed to
compute them. These values are then written to an output file.

"""
import argparse
import logging
import random
import time

import util

def betweenness_sample_size(graph, sample_size, set_attributes=True):
    """TODO """
    logging.info("Computing approximate betweenness using VC-Dimension, fixed sample size")
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_vc_sample_size(sample_size)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    stats["time"] = elapsed_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["vc_" + key] = stats[key]
        graph.vs["vc_betw"] = betw

    return (stats, betw)

def betweenness(graph, epsilon, delta, use_approx_diameter=True,
        set_attributes=True):
    """Compute approximate betweenness using VC-Dimension.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using sampling and the VC-Dimension, and the time needed to
    compute them, and some other statistics.

    Return a tuple with the statistics (a dictionary) and the list
    of betweenness values (one for each vertex in the graph).

    The meaning of the use_approx_diameter parameter is peculiar. If True or
    1 (default), compute an approximation of the diameter (only valid for
    undirected, unweighted graphs). If False or 0, compute
    the exact diameter (which kind of defeat the purpose of sampling, by the
    way). If any integer > 1, use this value for the diameter, i.e. do not
    perform any computation for the diameter.
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    logging.info("Computing approximate betweenness using VC-Dimension")
    if use_approx_diameter == 1:
        start_time = time.process_time()
        (stats, betw) = graph.betweenness_sample_vc(epsilon, delta, -1)
    elif use_approx_diameter == 0:
        start_time = time.process_time()
        diam = graph.diameter()
        (stats, betw) = graph.betweenness_sample_vc(epsilon, delta, diam)
    else:
        start_time = time.process_time()
        (stats, betw) = graph.betweenness_sample_vc(epsilon, delta, use_approx_diameter)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    stats["time"] = elapsed_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    stats["delta"] = delta
    if int(use_approx_diameter) == 1:
        stats["diam_type"] = "approx" 
    elif int(use_approx_diameter) == 0:
        stats["diam_type"] = "exact"
    else:
        stats["diam_type"] = "specif"
    stats["epsilon"] = epsilon

    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["vc_" + key] = stats[key]
        graph.vs["vc_betw"] = betw

    return (stats, betw)

def main():
    """Parse arguments, call betweenness(), write to file."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute approximate betweenness centrality of all vertices in a graph using sampling and VC-dimension, and the time to compute them, and write them to file"
    parser.add_argument("epsilon", type=util.valid_interval_float,
            help="accuracy parameter")
    parser.add_argument("delta", type=util.valid_interval_float,
            help="confidence parameter")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--approximate", action="store_true",
            default=True, help="use approximate diameter (default)")
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0,
            help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter")
    parser.add_argument("-s", "--samplesize", type=util.positive_int,
            default=0, help="use specified sample size. Overrides epsilon, delta, and diameter computation")
    parser.add_argument("-v", "--verbose", action="count", default=0,
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the approximate betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Seed the random number generator
    random.seed()

    # Read graph
    G = util.read_graph(args.graph)

    if args.exact:
        args.approximate = False

    # Compute betweenness
    if args.samplesize:
        (stats, betw) = betweenness_sample_size(G, args.samplesize, True)
    else:
        if args.diameter > 0:
            (stats, betw) = betweenness(G, args.epsilon, args.delta,
                    args.diameter, True)
        else:
            (stats, betw) = betweenness(G, args.epsilon, args.delta,
                    args.approximate, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write stats and betweenness to output
    util.write_to_output(stats, betw, args.output)

if __name__ == "__main__":
    main()

