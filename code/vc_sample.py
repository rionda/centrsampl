#! /usr/bin/env python3
"""vc_sample.py

Compute approximations of the betweenness centrality of all the vertices in
the graph using random sampling and the VC-dimension, and the time needed to
compute them. These values are then written to an output file.

"""
import argparse
import logging
import math
import os
import random
import time

import diameter_approx
import util

def get_sample_size(epsilon, delta, vcdim_upper_bound, c=0.5):
    """Compute sample size.

    Compute the sample size to achieve an epsilon-approximation of a range
    set with VC-dimension at most vcdim_upper_bound with probability at least
    1-delta.

    """
    return int(math.ceil((c / math.pow(epsilon, 2)) * ( vcdim_upper_bound +
        math.log(1 / delta) )))

def main():
    """Parse arguments, perform computation, write to file."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute approximate betweenness centrality of all vertices in a graph using sampling and VC-dimension, and the time to compute them, and write them to file"
    parser.add_argument("epsilon", type=util.valid_interval_float, help="graph file")
    parser.add_argument("delta", type=util.valid_interval_float, help="graph file")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the approximate betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="Use exact computation for the diameter (default)")
    group.add_argument("-a", "--approximate", action="store_true",
            default=False, help="Use approximate computation for the diameter")
    args = parser.parse_args()

    # Set the desired level of logging
    log_format='%(levelname)s: %(message)s'
    if args.verbose == 1:
        logging.basicConfig(format=log_format, level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(format=log_format, level=logging.DEBUG)

    # Read graph
    G = util.read_graph(args.graph)

    # Seed the random number generator
    random.seed()

    # Compute betweenness. We do not use logging from here to the end of the
    # computation to avoid wasting time (XXX right?)
    logging.info("Computing betweenness")
    betweenness = [0] * G.vcount()
    start_time = time.process_time()
    # Use desired diameter
    if args.approximate: # Use approximate diameter
        # Compute approx diameter if needed
        if not "approx_diam" in G.attributes():
            start_time_diam_approx = time.process_time()
            G["approx_diam"] = diameter_approx.diameter_approx(G)
            end_time_diam_approx = time.process_time()
            G["approx_diam_time"] = end_time_diam_approx - start_time_diam_approx
        # Compute VC-dimension upper bound using the approximate diameter
        vcdim_upp_bound = math.floor(math.log2(G["approx_diam"] -1)) # XXX Check
    else: # Use exact diameter
        # Compute exact diameter if needed
        if not "diam" in G.attributes():
            start_time_diam = time.process_time()
            # XXX What exactly does this compute? Especially for directed graphs
            G["diam"] = G.diameter() # This is not the vertex-diameter !!! 
            end_time_diam = time.process_time()
            G["diam_time"] = end_time_diam - start_time_diam
        vcdim_upp_bound = math.floor(math.log2(G["diam"] -1)) # XXX Check
    sample_size = get_sample_size(args.epsilon, args.delta, vcdim_upp_bound)
    sampled_paths = 0
    while sampled_paths < sample_size:
        # Sample a pair of different vertices uniformly at random
        sampled_pair = random.sample(range(G.vcount()), 2)
        # get_all_shortest_paths returns a list of shortest paths
        shortest_paths = G.get_all_shortest_paths(sampled_pair[0], sampled_pair[1]) 
        if shortest_paths:
            # Sample a shortest path uniformly at random
            sampled_path = random.sample(shortest_paths, 1)[0]
            # Update betweenness counters for vertices on the sampled path
            for vertex in sampled_path:
                betweenness[vertex] += 1
            # Increase number of sampled paths
            sampled_paths += 1
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Denormalize betweenness counters by (n choose 2) / k
    normalization = G.vcount() * (G.vcount() - 1) / (2 * sample_size)
    betweenness = list(map(lambda x : x * normalization, betweenness))

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.vs["vc_eps"] = args.epsilon
        G.vs["vc_delta"] = args.delta
        G.vs["vc_betw"] = betweenness
        G["vc_betw_time"] = elapsed_time
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

