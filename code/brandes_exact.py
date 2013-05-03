#! /usr/bin/env python3
"""brandes_exact.py

Compute the exact betweenness centrality of all vertices in a graph using
Brandes' algorithm and write it to a file, and the time needed to
compute the betweenness. These values are then written to an output file. For
Brandes' algorithm see
http://www.tandfonline.com/doi/abs/10.1080/0022250X.2001.9990249 .

"""
import argparse
import logging
import os
import time

import util

def betweenness(graph, set_attributes=True):
    """Compute exact betweenness of vertices in graph.
    
    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    # We do not use logging from here to the end of the computation to avoid
    # wasting time (XXX right?)
    logging.info("Computing betweenness")
    start_time = time.process_time()
    # XXX TODO Check whether multiple shortest paths are handled correctly!
    betw = graph.betweenness()
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computed in %s seconds", elapsed_time)

    if set_attributes:
        graph["betw_time"] = elapsed_time
        graph.vs["betw"] = betw
    return (elapsed_time, betw)

def main():
    """Parse arguments and perform the computation."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the exact betweenness centrality of all vertices in a graph using Brandes' algorithm, and the time to compute them, and write them to file"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # Compute betweenness
    (elapsed_time, betw) = betweenness(G, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file.
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write betweenness and time to output
    util.write_to_output(elapsed_time, betw, args.output)

if __name__ == "__main__":
    main()

