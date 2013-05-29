#! /usr/bin/env python3
# -*- coding: iso-8859-1 -*-
""" exact_experiment.py

    Perform experiment to evaluate Brandes' exact algorithm to compute the
    betweenness centrality of all vertices in a graph.
    The algorithm is run multiple times. We compute aggregate statistics about
    the runs and save the stats and all the results in a single .pickle file.
    
"""
import argparse
import logging
import math
import os.path
import pickle
import sys

import brandes_exact
import converter
import util

"""TODO"""

def main():
    """Parse arguments, run experiments, collect results and stats, write to file."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Perform experiment to compute exact betweenness centrality of all vertices in a graph using Brandes' algorithm"
    parser.add_argument("runs", type=util.positive_int, default=20, help="number of runs")
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
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    # Perform experiment multiple times
    results = []
    for i in range(args.runs):
        logging.info("Run #%d", i)
        results.append(brandes_exact.betweenness(G, False, args.timeout))

    # Compute aggregate statistics about the experiments
    stats = dict(results[0][0])
    stats["graph"]= os.path.basename(args.graph)
    stats["runs"] = args.runs
    del stats["time"]
    times = sorted([x[0]["time"] for x in results])
    stats["time_max"] = times[-1]
    stats["time_min"] = times[0]
    stats["time_avg"] = sum(times) / args.runs
    if args.runs > 1:
        stats["time_stddev"] = math.sqrt(sum([math.pow(time -
            stats["time_avg"], 2) for time in times]) / (args.runs - 1))
    else:
        stats["time_stddev"] = 0.0

    csvkeys="graph, runs, time_avg, time_stddev, time_max, time_min, forward_touched_edges, backward_touched_edges"
    print(csvkeys)
    print(util.dict_to_csv(stats, csvkeys))
    # Write stats and results to output file
    try: 
        with open(args.output, "wb") as output:
            logging.info("Writing stats and results to %s", args.output)
            pickle.dump((stats, results), output)
            output.close()
    except OSError as E:
        logging.critical("Cannot write stats and results to %s: %s",
                args.output, E.strerror)
        sys.exit(2)

if __name__ == "__main__":
    main()

