import argparse
import logging
import math
import os.path
import pickle
import sys

import brandes_exact
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
    parser.add_argument("-v", "--verbose", action="count", default=0, 
            help="increase verbosity (use multiple times for more verbosity)")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # Perform experiment multiple times
    results = []
    for i in range(args.runs):
        logging.info("Run #%d", i)
        results.append(brandes_exact.betweenness(G, False))

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
    print(util.dict_to_csv(stats, csvkeys))
    # Write stats and results to output file
    try: 
        with open(args.output, "wb") as output:
            logging.info("Writing stats and results to %s", args.output)
            pickle.dump((stats, results), output)
    except OSError as E:
        logging.critical("Cannot write stats and results to %s: %s",
                args.output, E.strerror)
        sys.exit(2)

if __name__ == "__main__":
    main()

