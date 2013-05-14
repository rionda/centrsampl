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
import os.path
import time

import converter
import timeout
import util

def do_betweenness(graph):
    start_time = time.process_time()
    (stats, betw) = graph.betweenness()
    end_time = time.process_time()
    stats["time"] = end_time - start_time
    return (stats,betw)

def betweenness(graph, set_attributes=True, time_out=0):
    """Compute exact betweenness of vertices in graph and statistics

    Return a tuple with the statistics (a dictionary) and the list of
    betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.

    """
    # We minimize the use of logging from here to the end of the computation to avoid
    # wasting time 
    logging.info("Computing exact betweenness")
    if not time_out:
        (stats, betw) = do_betweenness(graph)
    else:
        timeout_betweenness = timeout.add_timeout(do_betweenness, time_out)
        timeout_betweenness(graph)
        while (not timeout_betweenness.ready) and (not timeout_betweenness.expired):
            pass
        if timeout_betweenness.ready:
            (stats, betw) = timeout_betweenness.value
            logging.info("Betweenness computed in %s seconds", stats['time'])
            stats["timed_out"] = 0
        else:
            logging.info("Betweenness computation timer expired after %d seconds.", time_out)
            betw = [0] * graph.vcount()
            stats = {"time": time_out, "timed_out": 1, "forward_touched_edges": -1,
                    "backward_touched_edges": -1}

    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["exact_" + key] = stats[key]
        graph.vs["exact_betw"] = betw

    return (stats, betw)

def main():
    """Parse arguments and perform the computation."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute the exact betweenness centrality of all vertices in a graph using Brandes' algorithm, and the time to compute them, and write them to file"
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-t", "--timeout", type=util.positive_int, default=3600,
            help="Timeout computation after specified number of seconds (default 3600 = 1h, 0 = no timeout)")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    parser.add_argument("-v", "--verbose", action="count", default=0, 
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", nargs="?", default=False, const="auto",
            help="write graph (and computed attributes) to file.")
    args = parser.parse_args() 

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    # Compute betweenness
    (stats, betw) = betweenness(G, args.write, args.timeout)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file.
    if args.write:
        logging.info("Writing betweenness as vertex attributes and stats as graph attribute")
        if args.write == "auto":
            filename = os.path.splitext(args.graph)[0] + ("-undir" if args.undirected else "dir") + ".picklez"
            G.write(filename)
        else:
            G.write(args.write)

    # Write stats and betweenness to output
    util.write_to_output(stats, betw, args.output)

if __name__ == "__main__":
    main()

