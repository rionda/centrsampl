#! /usr/bin/env python3
"""geisberger_sample.py

Compute approximations of the betweenness centrality of all the vertices
in the graph using the algorithm by Robert Geisberger, Peter Sanders, Dominik
Schultes, linear scaling version. For the algorithm, see
http://www.siam.org/proceedings/alenex/2008/alx08_09geisbergerr.pdf .

"""
import argparse
import logging
import os.path
import time

import converter
import timeout
import util

def do_betweenness_sample_size(graph, sample_size):
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_gss_linear_sample_size(sample_size)
    end_time = time.process_time()
    stats["time"] = end_time - start_time
    return (stats, betw)

def betweenness_sample_size(graph, sample_size, set_attributes=True, time_out=0):
    """Compute approximate betweenness using Geisberger et al. algo, linear
    scaling version and a specified sample size."""
    logging.info("Computing approximate betweenness using GeisbergerSS algorithm, linear scaling fixed sample size")
    if not time_out:
        (stats, betw) = do_betweenness_sample_size(graph, sample_size)
    else:
        timeout_betweenness = timeout.add_timeout(do_betweenness_sample_size, time_out)
        timeout_betweenness(graph, sample_size)
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
                    "backward_touched_edges": -1, "sample_size": sample_size}
    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["bp_" + key] = stats[key]
        graph.vs["bp_betw"] = betw

    return (stats, betw)

def do_betweenness(graph, epsilon, delta):
    start_time = time.process_time()
    (stats, betw) = graph.betweenness_sample_gss_linear(epsilon, delta)
    end_time = time.process_time()
    stats["time"] = end_time - start_time
    return (stats, betw)

def betweenness(graph, epsilon, delta, set_attributes=True, time_out=0):
    """Compute approx. betweenness using BrandesGSS algorithm.
    
    Compute approximations of the betweenness centrality of all the vertices in
    the graph using the algorithm by Robert Geisberger, Peter Sanders, Dominik
    Schultes, and the time needed to compute them. For the algorithm, see
    http://www.siam.org/proceedings/alenex/2008/alx08_09geisbergerr.pdf .

    Return a tuple with various stats about the computation and the list
    of betweenness values (one for each vertex in the graph).
    If set_attributes is True (default), then set the values of the betweenness
    as vertex attributes, and the time as a graph attribute.
    
    """
    # We do not use logging from here to the end of the computation to avoid
    # wasting time
    logging.info("Computing approximate betweenness using GeisbergerSS, linear scaling algorithm")
    if not time_out:
        (stats, betw) = do_betweenness(graph, epsilon, delta)
    else:
        timeout_betweenness = timeout.add_timeout(do_betweenness, time_out)
        timeout_betweenness(graph, epsilon, delta)
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
                    "backward_touched_edges": -1, "sample_size": -1}

    stats["delta"] = delta
    stats["epsilon"] = epsilon
    # Write attributes to graph, if specified
    if set_attributes:
        for key in stats:
            graph["bp_" + key] = stats[key]
        graph.vs["bp_betw"] = betw

    return (stats, betw)

def main():
    """Parse arguments and perform the computation."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Compute approximate betweenness centrality of all vertices in a graph using the algorihm by Geisberger et al, linear scaling, and various stats to compute them, and write them to file"
    parser.add_argument("epsilon", type=util.valid_interval_float,
            help="accuracy parameter")
    parser.add_argument("delta", type=util.valid_interval_float,
            help="confidence parameter")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-s", "--samplesize", type=util.positive_int,
            default=0, help="use specified sample size. Overrides epsilon, delta, and diameter computation")
    parser.add_argument("-t", "--timeout", type=util.positive_int, default=3600,
            help="Timeout computation after specified number of seconds (default 3600 = 1h, 0 = no timeout)")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
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
    if args.samplesize:
        (stats, betw) = betweenness_sample_size(G, args.samplesize, args.write,
                args.timeout)
    else:
        (stats, betw) = betweenness(G, args.epsilon, args.delta, args.write,
                args.timeout)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
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

