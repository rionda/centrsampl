#! /usr/bin/env python3
""" diameter_approximation_motwani.py

Construct +++

"""
import argparse
import logging
import time

import util

def diameter_approximation_motwani(graph):
    logging.info("Computing diameter")
    # time.process_time() does not account for sleeping time. Seems the right
    # function to use. Alternative could be time.perf_counter()
    start_time = time.process_time()
    # Compute the diameter of the graph, i.e. the longest geodesic path within
    # a component.
    diam = graph.diameter_approximation_motwani() # This is not the vertex-diameter !!! 
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Diameter is %d, computed in %f seconds", diam, elapsed_time)
    return (elapsed_time,diam)

def main():
    """Parse arguments, call the diameter_approximation_motwani."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute an approximation of the diameter and output its value"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0,
            help="increase verbosity (use multiple times for more verbosity)")
    args = parser.parse_args()

    # Set the desired level of logging

    # Read graph from file                                   
    G = util.read_graph(args.graph)

    # Check if graph is directed and act accordingly
    # XXX We probably shouldn't do this!
    was_directed = False
    if G.is_directed():
        logging.warning("Graph is directed, running 2/3-approx for directed graphs")

    # Compute the 2/3 approximation
    (elapsed_time,diam) = diameter_approximation_motwani(G)

    # Print info
    print("{}, diameter={}, time={}".format(args.graph, diam,
        elapsed_time))
    # If requested, add graph attributes and write graph back to original file
   # if args.write:
       # logging.info("Writing diameter approximation and time to graph")
        # If the graph was directed and we converted it, re-read it
        #if was_directed:
           # G = ig.Graph.Read(args.graph)
        #G["approx_diam"] = diam
        #G["approx_diam_time"] = elapsed_time
        # We use format auto-detection, which should work given that it worked
        # when we read the file
        #G.write(args.graph)

if __name__ == "__main__":
    main()
