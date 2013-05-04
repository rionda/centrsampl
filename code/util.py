"""util.py

Various useful functions.
"""
import argparse
import heapq
import logging
import random
import sys
import igraph as ig

def random_shortest_path(graph, source, destination):
    """Return a random shortest path between source and destination.

    This function assumes that compute_shortest_paths_dijkstra has been called
    with the same source most recently.

    The returned shortest path is chosen uniformly at random among all those
    between source and destination.
    
    """
    # base case
    if graph.vs[destination]["preds"] == [graph.vs[source]]:
        return [source]
    # recursion step
    # Create balls to put in urn to choose predecessor
    balls = [0] * graph.vs[destination]["paths"]
    ball_index = 0
    for pred in graph.vs[destination]["preds"]:
        for i in range(pred["paths"]):
            balls[ball_index] = pred.index
            ball_index += 1
    # Draw a random ball to choose a predecessor to follow
    pred_index = random.sample(balls, 1)[0]
    # Compute predecessor shortest path 
    pred_sp = sample_random_shortest_path(graph, source, pred_index)

    return pred_sp.append(destination)

def get_all_shortest_paths(graph, source, destination):
    """Return all shortest paths between source and destination.
    
    This function assumes that compute_shortest_paths_dijkstra has been called
    with the same source most recently.

    Return a list of lists of vertex indexes, each list represents a path
    between source and destination.

    """
    # base case
    if graph.vs[destination]["preds"] == [graph.vs[source]]:
        return [[source]]
    # recursion step
    shortest_paths = [[]] * graph.vs[destination]["paths"]
    path_index = 0
    for pred in graph.vs[destination]["preds"]:
        pred_shortest_paths = get_all_shortest_paths(graph, source, graph.vs[pred].index)
        for path in pred_shortest_paths:
            shortest_paths[path_index] = path.append(destination)
            path_index += 1
    return shortest_paths

def compute_shortest_paths_dijkstra(graph, source, destination=None, weights=None):
    """Compute all shortest paths from a given source in the graph.
    
    Compute the shortest paths from source to all vertices in the graph or, if
    "to" is not None, to the specified vertex. "weights" can be edge weights in
    a list or the name of an edge attribute holding edge weights. If None, all
    edges are assumed to have unitary weight.

    The shortest paths between source and another vertex can be retrieved by
    walking back from 

    Return a list of vertices sorted by non-increasing distance from the
    source.

    TODO: Implement destination handling
    """  
    # Initialization
    # list of predecessors
    graph.vs["preds"] = [] * graph.vcount()
    # number of shortest paths through this node
    graph.vs["paths"] = [0] * graph.vcount ()
    graph.vs[source]["paths"] = 1
    # current distance from the source
    graph.vs["dist"] = [-1] * graph.vcount()
    graph.vs[source]["dist"] = 0
    # After the shortest paths computation, this stack can be used to return
    # vertices in order of non-increasing distance from the source. Useful for
    # betweenness computation.
    vertices_stack = []
    # distance-from-source min-proprity queue
    distance_heap = []
    # Take care of weights
    if weights == None:
        _weights = [1] * graph.ecount()
    else: 
        if weights in graph.edge_attributes():
            _weights = graph.es[weights]
        else:
            assert len(weights) == graph.ecount()
            _weights = weights

    heapq.heappush(distance_heap, (graph.vs[source]["dist"], graph.vs[source]))

    # Shortest paths computation 
    while distance_heap:
        vertex = heapq.heappop(distance_heap)
        vertices_stack.append(vertex)
        for neighbor in graph.neighbors(vertex):
            # Relax
            distance_from_vertex = _weights[graph.eid(vertex, neighbor)]
            # Is it the first time we see neighbor?
            if neighbor["dist"] == -1:
                # Update distance of neighbor from source
                neighbor["dist"] = vertex["dist"] + distance_from_vertex
                # Push neighbor to distance_heap
                heapq.heappush(distance_heap, (neighbor["dist"], neighbor))
            # shortest path to neighbor via vertex?
            if neighbor["dist"] == vertex["dist"] + distance_from_vertex:
                # Update number of paths from source to neighbor
                neighbor["paths"] += vertex["paths"]
                # Add vertex to the predecessors of neightbor
                neighbor["preds"].append(vertex)
    # Return the stack of vertices
    return vertices_stack
  
def positive_int(string):
    """Check validity of string as positive integer. Return value if it is.
    
    To be used as the value for "type" argument in argparse.add_argument().
    If string is valid, return int value of the string. Otherwise raise an
    argparse Error.

    """
    try:
        value = int(string)
        if value < 1:
            msg = "{} is not positive".format(string)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
           msg = "{} is not a valid int".format(string) 
           raise argparse.ArgumentTypeError(msg)
    return value

def read_graph(path):
    """Read an igraph.Graph from the file path. Return graph."""
    logging.info("Reading graph from %s", path) 
    try:
        G = ig.Graph.Read(path)
    except OSError as E:
        # XXX There seems to be some problem in the propagation of E.strerror,
        # so the following actually print None at the end. Not our fault. We
        # leave it here as perhaps it will be fixed upstream at some point.
        logging.critical("Cannot read graph file %s: %s", path, E.strerror)
        sys.exit(2)
    return G

def set_verbosity(level):
     """Set the desired level of logging."""

     log_format='%(levelname)s: %(message)s'
     if level == 1:
         logging.basicConfig(format=log_format, level=logging.INFO)
     elif level >= 2:
         logging.basicConfig(format=log_format, level=logging.DEBUG)

def valid_interval_float(string):
    """Check validity of string as float between 0 and 1 (extremes excluded).
    
    To be used as the value for "type" argument in argparse.add_argument().
    If string is valid, return float value of the string. Otherwise raise an
    argparse Error.

    """
    try:
        value = float(string)
        if value <= 0 or value >= 1:
            msg = "{} is not between 0 and 1 (extremes excluded)".format(string)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
           msg = "{} is not a valid float".format(string) 
           raise argparse.ArgumentTypeError(msg)
    return value

def write_to_output(elapsed_time, betw, output_path):
    """ Write time and betweenness to output file."""
    try:
        with open(output_path, 'wt') as output:
            logging.info("Writing time and betweenness to output file")
            output.write("({}, {})\n".format(betw, elapsed_time))
    except OSError as E:
        logging.critical("Cannot write betweenness to %s: %s", output_path,
                E.strerror)

