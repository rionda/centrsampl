#! /usr/bin/env python3
"""vc_sample.py

Compute approximations of the betweenness centrality of all the vertices in
the graph using random sampling and the VC-dimension, and the time needed to
compute them. These values are then written to an output file.

"""
import argparse
import logging
import math
import random
import time

import diameter
import diameter_approx
import util

def betweenness(graph, epsilon, delta, use_approx_diameter=True, set_attributes=True):
    """Compute approx. betweenness using VC-Dimension.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using sampling and the VC-Dimension, and the time needed to
    compute them. 

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing betweenness")
    # Seed the random number generator
    random.seed()
    betw = [0] * graph.vcount()
    start_time = time.process_time()
    # Use desired diameter
    if use_approx_diameter: # Use approximate diameter
        diameter_approx.diameter(graph)
        # Compute VC-dimension upper bound using the approximate diameter
        vcdim_upp_bound = math.floor(math.log2(graph["approx_diam"] - 1))
    else: # Use exact diameter
        diameter.diameter(graph) 
        vcdim_upp_bound = math.floor(math.log2(graph["diam"] - 1))
    sample_size = get_sample_size(epsilon, delta, vcdim_upp_bound)
    for i in range(sample_size):
        # Sample a pair of different vertices uniformly at random
        sampled_pair = random.sample(range(graph.vcount()), 2)
        # get_all_shortest_paths returns a list of shortest paths
        shortest_paths = graph.get_all_shortest_paths(sampled_pair[0], sampled_pair[1]) 
        # Only sample path and increment counter if there actually is at least
        # a paths between the two nodes. Otherwise, do nothing.
        if shortest_paths:
            # Sample a shortest path uniformly at random
            sampled_path = random.sample(shortest_paths, 1)[0]
            # Update betweenness counters for vertices on the sampled path
            for vertex in sampled_path:
                betw[vertex] += 1
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Denormalize betweenness counters by (n choose 2) / k
    normalization = graph.vcount() * (graph.vcount() - 1) / (2 * sample_size)
    betw = list(map(lambda x : x * normalization, betw))

    # Write attributes to graph, if specified
    if set_attributes:
        graph["vc_betw_time"] = elapsed_time
        graph["vc_delta"] = delta
        graph["vc_eps"] = epsilon
        graph["vc_type"] = "approx" if use_approx_diameter else "exact"
        graph.vs["vc_betw"] = betw

    return (elapsed_time, betw)

def get_sample_size(epsilon, delta, vcdim_upper_bound, c=0.5):
    """Compute sample size.

    Compute the sample size to achieve an epsilon-approximation of a range
    set with VC-dimension at most vcdim_upper_bound with probability at least
    1-delta.

    """
    return int(math.ceil((c / math.pow(epsilon, 2)) * ( vcdim_upper_bound +
        math.log(1 / delta) )))

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
            default=False, help="use approximate diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter (default)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the approximate betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # Compute betweenness
    (elapsed_time, betw) = betweenness(args.graph, args.epsilon, args.delta, args.approximate, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write betweenness and time to output
    util.write_to_output(elapsed_time, betw, args.output)

if __name__ == "__main__":
    main()

