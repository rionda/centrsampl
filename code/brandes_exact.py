#! /usr/bin/env python3
"""brandes_exact.py

Compute the exact betweenness centrality of all vertices in a graph using
Brandes' algorithm and write it to a file, and the time needed to
compute the betweenness. These values are then written to an output file. For
Brandes' algorithm see
http://www.tandfonline.com/doi/abs/10.1080/0022250X.2001.9990249 .

"""
import argparse
import itertools
import logging
import sys
import time

import util

def betweenness_igraph(graph, set_attributes=True):
    """Compute exact betweenness of vertices in graph and time needed.

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    igraph version using igraph.Graph.betweenness()

    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing exact betweenness with igraph implementation")
    start_time = time.process_time()
    betw = graph.betweenness()
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computed in %s seconds", elapsed_time)

    # If the graph is undirected, it seems that igraph only counts paths once
    # in one direction, so multiply betweenness values by 2. 
    # XXX Needs more checking
    if not graph.is_directed():
        logging.debug("Adjusting betweenness values for undirectness")
        betw = list(map(lambda x: x * 2, graph.betweenness()))
    
    # Write attributes to graph, if specified
    if set_attributes:
        graph["betw_time"] = elapsed_time
        graph.vs["betw"] = betw
        graph.vs["betw_type"] = "igraph"

    return (elapsed_time, betw)

def update_betweenness(graph, source, betw):
    """Update the betweenness using the contribution of the source.
    
    Update the betweenness of all vertices in the graph by adding the
    contribution of the specified source. The computation follows the
    description in Brandes's original paper, see
    http://dx.doi.org/10.1080/0022250X.2001.9990249 .

    Return the update betweenness.

    """ 
    deltas = [0] * graph.vcount()
    # Compute shortest paths
    vertices_stack = util.compute_shortest_paths_dijkstra(graph, source.index)
    while vertices_stack:
        vertex_index = vertices_stack.pop(-1)
        vertex = graph.vs[vertex_index]
        for pred_index in vertex["preds"]:
            deltas[pred_index] += (graph.vs[pred_index]["paths"] /
                    vertex["paths"]) * (1 + deltas[vertex_index])
        if vertex_index != source.index:
            betw[vertex_index] += deltas[vertex_index]
    return betw

def betweenness_homegrown(graph, set_attributes=True):
    """Compute exact betweenness of vertices in graph and time needed.

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    Completely homegrown version

    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing exact betweenness with homegrown implementation")
    betw = [0] * graph.vcount()
    start_time = time.process_time()
    # Compute betweenness.
    for source in graph.vs:
       betw = update_betweenness(graph, source, betw) 
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)
    
    # Write attributes to graph, if specified
    if set_attributes:
        graph["betw_time"] = elapsed_time
        graph.vs["betw"] = betw
        graph.vs["betw_type"] = "homegrown"
    
    return (elapsed_time, betw)

def vertex_betweenness_contribution(graph, vertex):
    """Compute the contribution of the given vertex to the betweenness of the
    vertices in the graph.
    
    Return a list containing the contribution of this vertex to the betweenness
    of each vertex of the graph.
    
    """
    contrib = [0] * graph.vcount()
    # get_all_shortest_paths returns a list of shortest paths
    shortest_paths = graph.get_all_shortest_paths(vertex) 
    # Group shortest paths by destination vertex, which is stored as the
    # last element of the list representing the path
    shortest_paths_by_destination = itertools.groupby(shortest_paths, lambda x : x[-1])
    for destination, group in shortest_paths_by_destination:
        paths = list(group)
        # addend: 1 / number of shortest paths between source and destination
        addend = 1 / len(paths)
        for path in paths:
            # Update betweenness counters for vertices internal to the path
                for vertex in path[1:-1]:
                    contrib[vertex] += addend
    return contrib

def betweenness_noigraph(graph, set_attributes=True):
    """Compute exact betweenness of vertices in graph and time needed.

    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    non-igraph version.

    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing exact betweenness with noigraph implementation")
    betw = [0] * graph.vcount()
    start_time = time.process_time()
    # Add the contribution of each vertex
    for vertex in graph.vs:
        betw = [ a + b for a,b in zip(betw, vertex_betweenness_contribution(graph, vertex))]
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    logging.info("Betweenness computation complete, took %s seconds",
            elapsed_time)
    
    # Write attributes to graph, if specified
    if set_attributes:
        graph["betw_time"] = elapsed_time
        graph.vs["betw"] = betw
        graph.vs["betw_type"] = "noigraph"
    
    return (elapsed_time, betw)

def betweenness(graph, implementation="igraph", set_attributes=True):
    """Compute exact betweenness of vertices in graph and time needed.
    
    Return a tuple with the time needed to compute the betweenness and the list
    of betweenness values (one for each vertex in the graph).
    Compute betweenness using the specified implementation (available: igraph,
    noigraph, homegrown).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    if implementation == "igraph" or implementation == "chomegrown":
        return betweenness_igraph(graph, set_attributes)
    elif implementation == "noigraph":
        return betweenness_noigraph(graph, set_attributes)
    elif implementation == "homegrown":
        return betweenness_homegrown(graph, set_attributes)
    else:
        logging.critical("Betweenness implementation not recognized: %s",
                implementation)
        sys.exit(2)

def main():
    """Parse arguments and perform the computation."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the exact betweenness centrality of all vertices in a graph using Brandes' algorithm, and the time to compute them, and write them to file"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-i", "--implementation", choices=["igraph",
        "noigraph", "homegrown", "chomegrown"], default="igraph", 
        help="use specified implementation of betweenness computation")
    parser.add_argument("-v", "--verbose", action="count", default=0, 
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
            help="store the betweenness as an attribute of each vertex the graph and the computation time as attribute of the graph, and write these to the graph file")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # Compute betweenness
    (elapsed_time, betw) = betweenness(G, args.implementation, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file.
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Write betweenness and time to output
    util.write_to_output(elapsed_time, betw, args.output)

if __name__ == "__main__":
    main()

