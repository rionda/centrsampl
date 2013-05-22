#! /usr/bin/env python3
"""vc_sample.py

Compute approximations of the betweenness centrality of all the vertices in
the graph using random sampling and the VC-dimension, and the time needed to
compute them. These values are then written to an output file.

"""
import argparse
import logging
import os.path
import random
import time

import converter
import timeout
import util

def do_betweenness_sample_size(graph, sample_size):
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_vc_sample_size(sample_size)
    end_time = time.process_time()
    stats["time"] = end_time - start_time
    return (stats, betw)

def betweenness_sample_size(graph, sample_size, set_attributes=True, time_out=0):
    """Compute approximate betweenness using VC-Dimension and a specified sample size."""
    logging.info("Computing approximate betweenness using VC-Dimension, fixed sample size")
    if not time_out:
        (stats, betw) = do_betweenness_sample_size(graph, sample_size)
    else:
        timeout_betweenness = timeout.add_timeout(do_betweenness_sample_size, time_out)
        timeout_betweenness(graph, sample_size)
        while (not timeout_betweenness.ready) and (not timeout_betweenness.expired):
            pass
        if timeout_betweenness.ready:
            logging.info("Betweenness computed in %s seconds", stats['time'])
            (stats, betw) = timeout_betweenness.value
            stats["timed_out"] = 0
        else:
            logging.info("Betweenness computation timer expired after %d seconds.", time_out)
            betw = [0] * graph.vcount()
            stats = {"time": time_out, "timed_out": 1, "forward_touched_edges": -1,
                    "backward_touched_edges": -1, "sample_size": sample_size}

    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["vc_" + key] = stats[key]
        graph.vs["vc_betw"] = betw

    return (stats, betw)

def do_betweenness(graph, epsilon, delta, use_approx_diameter):
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
    stats["time"] = end_time - start_time
    return (stats, betw)

def betweenness(graph, epsilon, delta, use_approx_diameter=True,
        set_attributes=True, time_out=0):
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
    if not time_out:
        (stats, betw) = do_betweenness(graph, epsilon, delta,
                use_approx_diameter)
    else:
        timeout_betweenness = timeout.add_timeout(do_betweenness, time_out)
        timeout_betweenness(graph, epsilon, delta, use_approx_diameter)
        while (not timeout_betweenness.ready) and (not timeout_betweenness.expired):
            pass
        if timeout_betweenness.ready:
            (stats, betw) = timeout_betweenness.value
            logging.info("Betweenness computed in %s seconds", stats['time'])
            stats["timed_out"] = 0
        else:
            logging.info("Betweenness computation timer expired after %d seconds.", time_out)
            betw = [0] * graph.vcount()
            stats = {"time": time_out, "timed_out": 1, "forward_touched_edges": -1,
                    "backward_touched_edges": -1, "sample_size": -1,
                    "diameter": -1, "diameter_touched_edges": -1 }
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
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-s", "--samplesize", type=util.positive_int,
            default=0, help="use specified sample size. Overrides epsilon, delta, and diameter computation")
    parser.add_argument("-t", "--timeout", type=util.positive_int, default=3600,
            help="Timeout computation after specified number of seconds (default 3600 = 1h, 0 = no timeout)")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    parser.add_argument("-v", "--verbose", action="count", default=0,
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", nargs="?", default=False, const="auto",
            help="write graph (and computed attributes) to file.")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Seed the random number generator
    random.seed()

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    if args.exact:
        args.approximate = False

    # Compute betweenness
    if args.samplesize:
        (stats, betw) = betweenness_sample_size(G, args.samplesize, args.write)
    else:
        if args.diameter > 0:
            (stats, betw) = betweenness(G, args.epsilon, args.delta,
                    args.diameter, args.write)
        else:
            (stats, betw) = betweenness(G, args.epsilon, args.delta,
                    args.approximate, args.write)

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

