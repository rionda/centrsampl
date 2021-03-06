#! /usr/bin/env python3
"""diameter_approx.py

Compute an approximation of the diameter of a graph (upper bound, at most 2
times the exact value) and the time needed to compute it, and write these info
as graph attributes. The graph should be undirected and have unitary edge
weights.

"""
import argparse
import logging
import random
import sys
import time
import igraph as ig

import converter
import util

def diameter_homegrown(graph, weights=None):
    """Compute diameter approximation and time needed to compute it.

    Return a tuple (elapsed_time, diam), where elapsed_time is the time (in
    fractional seconds) needed to compute the approximation to the diameter of
    the graph.

    To compute the approximation, we sample a vertex uniformly at random,
    compute the shortest paths from this vertex to all other vertices, and sum
    the lengths of the two longest paths we found. The returned value is an
    upper bound to the diameter of the graph and is at most 2 times the exact
    value.

    If sample_path is True, sample one of the shortest paths computed for the
    approximation, and set it as graph attribute.

    Homegrown version
    
    """
    logging.info("Computing diameter approximation with igraph implementation")
    # time.process_time() does not account for sleeping time. Seems the right
    # function to use. Alternative could be time.perf_counter()
    start_time = time.process_time()
    diam = graph.diameter_approximation(weights)
    end_time =  time.process_time()
    elapsed_time = end_time - start_time

    logging.info("Diameter approximation is %d, computed in %f seconds", diam, elapsed_time)
    graph["approx_diam"] = diam
    graph["approx_diam_time"] = elapsed_time
    return (elapsed_time, diam)

def diameter_igraph(graph, sample_path=False):
    """Compute diameter approximation and time needed to compute it.

    Return a tuple (elapsed_time, diam), where elapsed_time is the time (in
    fractional seconds) needed to compute the approximation to the diameter of
    the graph.

    To compute the approximation, we sample a vertex uniformly at random,
    compute the shortest paths from this vertex to all other vertices, and sum
    the lengths of the two longest paths we found. The returned value is an
    upper bound to the diameter of the graph and is at most 2 times the exact
    value.

    If sample_path is True, sample one of the shortest paths computed for the
    approximation, and set it as graph attribute.

    igraph version
    
    """
    logging.info("Computing diameter approximation with igraph implementation")
    # time.process_time() does not account for sleeping time. Seems the right
    # function to use. Alternative could be time.perf_counter()
    start_time = time.process_time()
    # sample a vertex uniformly at random
    sampled_vertex = graph.vs[random.randint(0, len(graph.vs)-1)]
    # We convert the list to a set to remove duplicates
    shortest_paths = graph.get_all_shortest_paths(sampled_vertex)
    shortest_path_lengths = frozenset(map(lambda x : len(x) - 1, shortest_paths)) 
    diam = max(shortest_path_lengths)
    diam += max(shortest_path_lengths - frozenset([diam]))
    end_time = time.process_time()
    elapsed_time = end_time - start_time

    logging.info("Diameter approximation is %d, computed in %f seconds", diam, elapsed_time)
    graph["approx_diam"] = diam
    graph["approx_diam_time"] = elapsed_time

    # If required, sample a path among the shortest paths. Useful to minimally
    # speed up betweenness computation 
    # TODO Test if it actually speeds things up
    if sample_path:
        graph["sampled_path"] = random.sample(shortest_paths[1:], 1)[0]

    return (elapsed_time, diam)

def diameter(graph, implementation="igraph", sampled_path=True):
    """Compute diameter approximation and time needed to compute it.

    Return a tuple (elapsed_time, diam), where elapsed_time is the time (in
    fractional seconds) needed to compute the approximation to the diameter of
    the graph.

    To compute the approximation, we sample a vertex uniformly at random,
    compute the shortest paths from this vertex to all other vertices, and sum
    the lengths of the two longest paths we found. The returned value is an
    upper bound to the diameter of the graph and is at most 2 times the exact
    value.

    Use the specified implementation to compute the approximation (available:
    igraph, homegrown)

    (only igraph implementation) If sample_path is True, sample one of the
    shortest paths computed for the approximation, and set it as graph
    attribute.

    """
    if implementation == "igraph":
        return diameter_igraph(graph, sampled_path)
    elif implementation == "homegrown":
        return diameter_homegrown(graph)
    else:
        logging.critical("Betweenness implementation not recognized: %s",
                implementation)
        sys.exit(2)

def main():
    """Parse arguments, call the approximation, write it to file."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute an approximation of the diameter of a graph and the time needed to compute it, and (if specified) write these info as a graph attributes"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-i", "--implementation", choices=["homegrown",
        "igraph"], default="homegrown", 
        help="use specified implementation of betweenness computation")
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    parser.add_argument("-v", "--verbose", action="count", default=0, 
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
    help="write the approximation of diameter of the graph as the 'approx_diameter' graph attribute and the time taken to compute it as the 'approx_diam_time' attribute")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Seed the random number generator
    random.seed()

     # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)   # Read graph from file

    # Compute the diameter
    (elapsed_time, diam) = diameter(G, args.implementation)

    # Print info
    print("{}, diameter={}, time={}".format(args.graph, diam, elapsed_time))

    # If requested, add graph attributes and write graph back to original file
    if args.write:
        logging.info("Writing diameter approximation and time to graph")
        G["approx_diam"] = diam
        G["approx_diam_time"] = elapsed_time
        # We use format auto-detection, which should work given that it worked
        # when we read the file
        G.write(args.graph) 

if __name__ == "__main__":
    main()


