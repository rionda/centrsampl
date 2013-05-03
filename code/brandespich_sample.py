#! /usr/bin/env python3
"""brandespich_sample.py

Compute approximations of the betweenness centrality of all the vertices
in the graph using the algorithm by Brandes and Pich, and the time needed to
compute them. These values are then written to an output file. For the
algorihm, see http://www.worldscientific.com/doi/abs/10.1142/S0218127407018403 .

"""
import argparse
import itertools
import logging
import math
import os
import random
import time

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
    # wasting time (XXX right?)
    logging.info("Computing betweenness")
    # Seed the random number generator
    random.seed()
    betw = [0] * graph.vcount()
    start_time = time.process_time()
    sample_size = get_sample_size(epsilon, delta, graph.vcount())
    for i in range(sample_size):
        # Sample a source vertex uniformly at random
        sampled_vertex = random.randrange(graph.vcount())
        # get_all_shortest_paths returns a list of shortest paths
        shortest_paths = graph.get_all_shortest_paths(sampled_vertex) 
        # Group shortest paths by destination vertex, which is stored as the
        # last element of the list representing the path
        grouped_shortest_paths = itertools.groupby(shortest_paths, lambda x : x[-1])
        for destination, group in grouped_shortest_paths:
            paths = list(group)
            # addend: 1 / number of shortest paths between source and destination
            addend = 1 / len(paths)
            for path in paths:
                # Update betweenness counters for vertices internal to the path
                for vertex in path[1:-1]:
                    betw[vertex] += addend
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)

    # Denormalize betweenness counters by n / k
    normalization = graph.vcount() / sample_size 
    betw = list(map(lambda x : x * normalization, betw))

    # Write attributes to graph, if specified
    if set_attributes:
        graph["bp_betw_time"] = elapsed_time
        graph["bp_delta"] = delta
        graph["bp_eps"] = epsilon
        graph.vs["bp_betw"] = betw

    return (elapsed_time, betw)

def get_sample_size(epsilon, delta, vertices_num):
    """Compute sample size.
    
    Compute the sample size to achieve an epsilon-approximation of for the
    betweenness centralities of the vertices of a graph with vertices_num
    vertices, with probability at least 1-delta. The formula is taken by
    applying an Hoeffding bound.

    """
    return int(math.ceil((2 * math.pow((vertices_num - 2) / (epsilon *
        (vertices_num - 1)), 2) * math.log(2 * vertices_num / delta))))

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
    (elapsed_time, betw) = betweenness(G, args.epsilon, args.delta, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write betweenness and time to output
    util.write_to_output(elapsed_time, betw, args.output)

if __name__ == "__main__":
    main()

