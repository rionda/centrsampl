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
import sys
import time

import diameter
import diameter_approx
import util

def betweenness_homegrown(graph, epsilon, delta, use_approx_diameter=True,
        set_attributes=True):
    """Compute approximate betweenness using VC-Dimension.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using sampling and the VC-Dimension, and the time needed to
    compute them. 

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).

    The meaning of the use_approx_diameter parameter is peculiar. If True or
    1 (default), compute an approximation of the diameter (only valid for
    undirected, unweighted graphs). If False or 0, compute
    the exact diameter (which kind of defeat the purpose of sampling, by the
    way). If any integer > 1, use this value for the diameter, i.e. do not
    perform any computation for the diameter.
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    Homegrown version
    
    """
    logging.info("Computing approximate betweenness using VC-Dimension, homegrown implementation")
    if use_approx_diameter == 1:
        start_time = time.process_time()
        betw = graph.betweenness_sample_vc(epsilon, delta, -1)
    elif use_approx_diameter == 0:
        start_time = time.process_time()
        diam = graph.diameter()
        betw = graph.betweenness_sample_vc(epsilon, delta, diam)
    else:
        start_time = time.process_time()
        betw = graph.betweenness_sample_vc(epsilon, delta, use_approx_diameter)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Write attributes to graph, if specified
    if set_attributes:
        graph["vc_betw_time"] = elapsed_time
        graph["vc_delta"] = delta
        if int(use_approx_diameter) == 1:
            graph["vc_diam_type"] = "approx" 
        elif int(use_approx_diameter) == 0:
            graph["vc_diam_type"] = "exact"
        else:
            graph["vc_diam_type"] = "specif"
        graph["vc_eps"] = epsilon
        graph["vc_type"] = "homegrown"
        graph.vs["vc_betw"] = betw

    return (elapsed_time, betw)

def betweenness_igraph(graph, epsilon, delta, use_approx_diameter=True, set_attributes=True):
    """Compute approximate betweenness using VC-Dimension.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using sampling and the VC-Dimension, and the time needed to
    compute them. 

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).

    The meaning of the use_approx_diameter parameter is peculiar. If True or
    1 (default), compute an approximation of the diameter (only valid for
    undirected, unweighted graphs). If False or 0, compute
    the exact diameter (which kind of defeat the purpose of sampling, by the
    way). If any integer > 1, use this value for the diameter, i.e. do not
    perform any computation for the diameter.
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    igraph version
    
    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing approximate betweenness using VC-Dimension, igraph version")

    betw = [0] * graph.vcount()
    sampled_path = False
    start_time = time.process_time()
    # Use desired diameter
    if int(use_approx_diameter) == 1: # Use approximate diameter
        diameter_approx.diameter(graph, sample_path=True)
        sampled_path = True
        # Update betweenness counters for vertices internal of the sampled path
        for vertex in graph["sampled_path"][1:-1]:
                betw[vertex] += 1
        # Compute VC-dimension upper bound using the approximate diameter
        vcdim_upp_bound = math.floor(math.log2(graph["approx_diam"] - 1))
    elif int(use_approx_diameter) == 0: # Use exact diameter
        diameter.diameter(graph) 
        vcdim_upp_bound = math.floor(math.log2(graph["diam"] - 1))
    elif int(use_approx_diameter) > 1: # Use specified diameter
        # Set the appropriate graph attributes explicitly, given that we don't
        # call any diameter function
        graph["vc_diam"] = use_approx_diameter
        graph["diam_time"] = 0
        vcdim_upp_bound = math.floor(math.log2(use_approx_diameter -1) + 1)
        # Set the appropriate graph attributes explicitly, given that we don't call
    else: # int(use_approx_diameter) < 0
        logging.critical("got negative diameter explicitly passed. Exiting")
        sys.exit(2)
    sample_size = get_sample_size(epsilon, delta, vcdim_upp_bound)
    # Adjust if we got a sample while computing the approximate diameter
    if sampled_path:
        sample_size -= 1
    for i in range(sample_size):
        # Sample a pair of different vertices uniformly at random
        sampled_pair = random.sample(range(graph.vcount()), 2)
        # get_all_shortest_paths returns a list of shortest paths
        shortest_paths = graph.get_all_shortest_paths(sampled_pair[0],
                sampled_pair[1]) 
        # Only sample path and increment counter if there actually is at least
        # a paths between the two nodes. Otherwise, do nothing.
        if shortest_paths:
            # Sample a shortest path uniformly at random
            sampled_path = random.sample(shortest_paths, 1)[0]
            # Update betweenness counters for vertices internal of the sampled path
            for vertex in sampled_path[1:-1]:
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
        if int(use_approx_diameter) == 1:
            graph["vc_diam_type"] = "approx" 
        elif int(use_approx_diameter) == 0:
            graph["vc_diam_type"] = "exact"
        else:
            graph["vc_diam_type"] = "specif"
        graph["vc_eps"] = epsilon
        graph["vc_type"] = "igraph"
        graph.vs["vc_betw"] = betw

    return (elapsed_time, betw)

def betweenness(graph, epsilon, delta, use_approx_diameter=True,
        implementation="igraph",  set_attributes=True):
    """ TODO """
    if implementation == "igraph":
        return betweenness_igraph(graph, epsilon, delta, use_approx_diameter,
                set_attributes)
    elif implementation == "homegrown":
        return betweenness_homegrown(graph, epsilon, delta,
                use_approx_diameter, set_attributes)
    else:
        logging.critical("Betweenness implementation not recognized: %s",
                implementation)
        sys.exit(2)

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
            default=True, help="use approximate diameter (default)")
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0,
            help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter")
    parser.add_argument("-i", "--implementation",
            choices=["homegrown","igraph"], default="homegrown", 
        help="use specified implementation of betweenness computation")
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
    if args.diameter > 0:
        (elapsed_time, betw) = betweenness(G, args.epsilon,
                args.delta, args.diameter, args.implementation, True)
    else:
        (elapsed_time, betw) = betweenness(G, args.epsilon,
                args.delta, args.approximate, args.implementation, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write betweenness and time to output
    util.write_to_output(elapsed_time, betw, args.output)

if __name__ == "__main__":
    main()

