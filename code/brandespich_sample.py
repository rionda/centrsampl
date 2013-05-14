#! /usr/bin/env python3
"""brandespich_sample.py

Compute approximations of the betweenness centrality of all the vertices
in the graph using the algorithm by Brandes and Pich, and the time needed to
compute them. These values are then written to an output file. For the
algorithm, see http://www.worldscientific.com/doi/abs/10.1142/S0218127407018403 .

"""
import argparse
import logging
import os.path
import time

import converter
import util

def betweenness_sample_size(graph, sample_size, set_attributes=True):
    """TODO """
    logging.info("Computing approximate betweenness using Brandes and Pich algorithm, fixed sample size")
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_bp_sample_size(sample_size)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    stats["time"] = elapsed_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["bp_" + key] = stats[key]
        graph.vs["bp_betw"] = betw

    return (stats, betw)

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
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-s", "--samplesize", type=util.positive_int,
            default=0, help="use specified sample size. Overrides epsilon, delta, and diameter computation")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the approximate betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    # Compute betweenness
    if args.samplesize:
        (stats, betw) = betweenness_sample_size(G, args.samplesize, True)
    else:
        (stats, betw) = betweenness(G, args.epsilon, args.delta, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and stats as graph attribute")
        if args.write == "auto":
            filename = os.path.splitext(args.graph)[0] + ("-undir" if args.undirected else "dir") + ".picklez"
            G.write(filename)
        else:
            G.write(args.write)

    # Write stats and betweenness to output
    util.write_to_output(stats, betw, args.output)

if __name__ == "__main__":
    main()

