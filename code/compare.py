#! /usr/bin/env python3
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import itertools
import logging
import math
import random

import util
import brandes_exact
import brandespich_sample
import vc_sample

def main():
    """Parse arguments, do the comparison, write to output."""
    parser = argparse.ArgumentParser()
    parser.description = "compare estimation of betweenness centralities to exact values"
    parser.add_argument("epsilon", type=util.valid_interval_float, help="accuracy parameter")
    parser.add_argument("delta", type=util.valid_interval_float, help="confidence parameter")
    parser.add_argument("graph", help="graph file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--approximate", action="store_true",
            default=False, help="use approximate diameter when computing approximation of betweenness using VC-Dimension")
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0, help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter when computing approximation of betweenness using VC-Dimension (default)")
    parser.add_argument("-f", "--force", action="store_true", default=False,
            help="Force recomputation of all betweenness values, exact and approximate.")
    parser.add_argument("-i", "--implementation", choices=["igraph",
        "homegrown"], default="igraph", 
        help="use specified implementation of betweenness computation")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--write", action="store_true", default=False,
    help="write the betweenness and the time taken to compute them (if needed) back to file")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Seed the random number generator
    random.seed()

    # Read graph
    G = util.read_graph(args.graph)

    # If the graph does not have the attributes for the betweenness or has the
    # wrong ones, (re-)compute them
    logging.info("Recomputing betweenness if needed")
    if args.force or not "betw_time" in G.attributes():
        brandes_exact.betweenness(G, args.implementation, True)
    if args.force or not "vc_betw_time" in G.attributes() or G["vc_eps"] != args.epsilon or G["vc_delta"] != args.delta:
        if args.diameter > 0:
            vc_sample.betweenness(G, args.epsilon, args.delta, args.diameter,
                    args.implementation, True)
        else:
            vc_sample.betweenness(G, args.epsilon, args.delta,
                    args.approximate, args.implementation, True)
    if args.force or not "bp_betw_time" in G.attributes() or G["bp_eps"] != args.epsilon or G["bp_delta"] != args.delta:
        brandespich_sample.betweenness(G, args.epsilon, args.delta,
                args.implementation, True)

    # If specified, write betweenness as vertex attributes, and time as graph
    # attribute back to file
    if args.write:
        logging.info("Writing betweenness as vertex attributes and time as graph attribute")
        G.write(args.graph)

    # Compute error statistics
    # It is not a problem to sort the error by value because we only compute
    # aggregates.
    logging.info("Computing error statistics")
    vc_errs = sorted([abs(a - b) for a,b in zip(G.vs["betw"],G.vs["vc_betw"])])
    vc_err_avg = sum(vc_errs) / G.vcount()
    vc_err_max = vc_errs[-1]
    vc_err_min = list(itertools.filterfalse(lambda x: x == 0, vc_errs))[0]
    vc_err_stddev = math.sqrt(sum([math.pow(err - vc_err_avg, 2) for err in vc_errs]) / (G.vcount() -1))
    vc_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
        G.vcount() * (G.vcount() - 1) / 2, vc_errs)))

    bp_errs = sorted([abs(a - b) for a,b in zip(G.vs["betw"],G.vs["bp_betw"])])
    bp_err_avg = sum(bp_errs) / G.vcount()
    bp_err_max = max(bp_errs)
    bp_err_min = list(itertools.filterfalse(lambda x: x == 0, bp_errs))[0]
    bp_err_stddev = math.sqrt(sum([math.pow(err - bp_err_avg, 2) for err in bp_errs]) / (G.vcount() -1))
    bp_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
        G.vcount() * (G.vcount() - 1) / 2, bp_errs)))

    # Print statistics to output as CSV
    logging.info("Printing error statistics")
    print("exact, {}, 0, 0".format(G["betw_time"]))
    print("vc, {}".format(", ".join([str(x) for x in [G["vc_betw_time"], vc_wrong_eps, vc_err_max,
        vc_err_min, vc_err_avg, vc_err_stddev]])))
    print("bp, {}".format(", ".join([str(x) for x in [G["bp_betw_time"], bp_wrong_eps, bp_err_max,
        bp_err_min, bp_err_avg, bp_err_stddev]])))
    
if __name__ == "__main__":
    main()

