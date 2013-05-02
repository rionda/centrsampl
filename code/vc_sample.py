#! /bin/env python3

import argparse
import logging
import math
import os
import random
import time
import igraph as ig

def get_sample_size(epsilon, delta, vcdim_upper_bound, c=0.5):
    """ Compute the sample size to achieve an epsilon-approximation of a range
    set with VC-dimension at most vcdim_upper_bound with probability at least 1-delta
    """
    return (c / math.pow(epsilon, 2)) * ( vcdim_upper_bound + math.log(1 / delta) )

def main():
    """Compute approximations of the betweenness centrality of all the vertices  
    in the graph using random sampling and the VC-dimension
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute approximate betweenness centrality of all vertices in a graph using sampling and VC-dimension, and the time to compute them, and write them to file"
    parser.add_argument("epsilon", type=float, help="graph file")
    parser.add_argument("delta", type=float, help="graph file")
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
    logging.info("Reading graph from %s", args.graph)
    G = ig.Graph.Read(args.graph)

    # Seed the random number generator
    random.seed()

    # Compute betweenness
    logging.info("Computing betweenness")
    start_time = time.process_time()
    if args.approximate:
        # TODO compute / use approx diameter 
        pass
    else:
        # TODO compute / use exact diameter 
        pass
    vcdim_upp_bound = 0 # XXX
    sample_size = get_sample_size(args.epsilon, args.delta, vcdim_upp_bound)
    for i in range(sample_size):
        # Sample a pair of different vertices uniformly at random
        sampled_pair = random.sample(G.vs, 2)
        # XXX Need to check what this does
        shortest_paths = G.get_all_shortest_paths(sampled_pair[u], sampled_pair[v]) 
        # TODO Finish computation

    betweenness = []
    end_time = time.process_time()
    elapsed_time = end_time - start_time


    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
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

