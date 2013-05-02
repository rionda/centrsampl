#! /bin/env python3

import argparse
import logging
import random
import time
import igraph as ig

def diameter_approx(graph):
    """ Return an approximation (upper bound) of the diameter of the graph"""
    sampled_vertex = graph.vs[random.randint(0, len(G.vs)-1)]
    # We convert the list to a set to remove duplicates
    shortest_path_lengths = set(G.shortest_paths_dijkstra([sampled_vertex])[0]) - set([float('inf')])
    diameter = max(shortest_path_lengths)
    diameter += max(shortest_path_lengths - set([diameter]))
    return diameter

def main():
    """Compute an approximation of diameter of the graph and the time needed to compute it, and
    write these info as  graph attributes.
    
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute an approximation of the diameter of a graph and the time needed to compute it, and (if specified) write these info as a graph attributes"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
    help="write the approximation of diameter of the graph as the 'approx_diameter' graph attribute and the time taken to compute it as the 'approx_diam_time' attribute")
    args = parser.parse_args()

    # Set the desired level of logging
    log_format='%(levelname)s: %(message)s'
    if args.verbose == 1:
        logging.basicConfig(format=log_format, level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(format=log_format, level=logging.DEBUG)

    # Read graph from file, using auto-detection of format
    logging.info("Reading graph from %s", args.graph) 
    G = ig.Graph.Read(args.graph)

    # Check if graph is directed and act accordingly
    was_directed = False
    if G.is_directed():
        logging.warning("Graph is directed, converting it to undirected")
        G.to_undirected()
        was_directed = True

    # Seed the random number generator
    random.seed()

    # Compute the diameter
    logging.info("Computing diameter")
    # time.process_time() does not account for sleeping time. Seems the right
    # function to use. Alternative could be time.perf_counter()
    start_time = time.process_time()
    # sample a vertex uniformly at random
    diameter = diameter_approx(G)
    end_time = time.process_time()
    elapsed_time = end_time - start_time

    # Print info
    logging.info("Diameter approximation is %d, computed in %f seconds", diameter,
            elapsed_time)
    print("{}, diameter={}, time={}".format(args.graph, diameter,
        elapsed_time))

    # If requested, add graph attributes and write graph back to original file
    if args.write:
        logging.info("Writing diameter approximation and time to graph")
        # If the graph was directed and we converted it, re-read it
        if was_directed:
            G = ig.Graph.Read(args.graph)
        G["approx_diameter"] = diameter
        G["approx_diam_time"] = elapsed_time
        # We use format auto-detection, which should work given that it worked
        # when we read the file
        G.write(args.graph) 

if __name__ == "__main__":
    main()


