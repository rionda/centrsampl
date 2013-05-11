#! /usr/bin/env python3
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import itertools
import logging
import math
import random

import diameter
import brandes_exact
import brandespich_sample
import util
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
            default=True, help="use approximate diameter when computing approximation of betweenness using VC-Dimension (default)")
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0, help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter when computing approximation of betweenness using VC-Dimension")
    parser.add_argument("-r", "--resultfiles", nargs=3, 
    help="Use results files rather than recomputing betweenness. Files should be specified as 'exact_res vc_res bp_res'")
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

    if args.exact:
        args.approximate = False

    if not args.resultfiles:
        (exact_stats, exact_betw) = brandes_exact.betweenness(G, True)
        if args.diameter > 0:
            (vc_stats, vc_betw) = vc_sample.betweenness(G, args.epsilon, args.delta,
                    args.diameter, True)
        else:
            (vc_stats, vc_betw) = vc_sample.betweenness(G, args.epsilon, args.delta,
                    args.approximate, True)
        (bp_stats, bp_betw) = brandespich_sample.betweenness(G, args.epsilon, args.delta,
                True)
    else:
        (exact_stats, exact_betw) = util.read_stats_betw(args.result_files[0])
        (vc_stats, vc_betw) = util.read_stats_betw(args.result_files[1])
        (bp_stats, bp_betw) = util.read_stats_betw(args.result_files[2])

    #Compute useful graph statistics (mainly diameter)
    if "diam" not in G.attributes():
        diameter.diameter(G)

    # If specified, write betweenness as vertex attributes, and time and
    # diameter as graph attributes back to file
    if args.write:
        logging.info("Writing graph back to file")
        G.write(args.graph)

    # Compute error statistics
    # It is not a problem to sort the error by value because we only compute
    # aggregates.
    logging.info("Computing error statistics")
    vc_errs = sorted([abs(a - b) for a,b in zip(exact_betw,vc_betw)])
    vc_stats["err_avg"] = sum(vc_errs) / G.vcount()
    vc_stats["err_max"] = vc_errs[-1]
    vc_stats["err_min"] = list(itertools.filterfalse(lambda x: x == 0, vc_errs))[0]
    vc_stats["err_stddev"] = math.sqrt(sum([math.pow(err - vc_stats["err_avg"], 2) for err in vc_errs]) / (G.vcount() -1))
    #vc_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
    #    G.vcount() * (G.vcount() - 1) / 2, vc_errs)))
    vc_stats["wrong_eps"] = 0;
    print("## VC wrong epsilon ##")
    for i in range(G.vcount()):
        err = abs(exact_betw[i] - vc_betw[i])
        if err > args.epsilon * G.vcount() * (G.vcount() - 1) / 2:
            vc_stats["wrong_eps"] += 1
            print("{} {} {} {} {} {} {}".format(i, G.vs[i].degree(),
                exact_betw[i], vc_betw[i], bp_betw[i],
                err, err / (G.vcount() * (G.vcount() -1) / 2)))

    bp_errs = sorted([abs(a - b) for a,b in zip(exact_betw,bp_betw)])
    bp_stats["err_avg"] = sum(bp_errs) / G.vcount()
    bp_stats["err_max"] = max(bp_errs)
    bp_stats["err_min"] = list(itertools.filterfalse(lambda x: x == 0, bp_errs))[0]
    bp_stats["err_stddev"] = math.sqrt(sum([math.pow(err - bp_stats["err_avg"], 2) for err in bp_errs]) / (G.vcount() -1))
    #bp_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
    #    G.vcount() * (G.vcount() - 1) / 2, bp_errs)))
    bp_stats["wrong_eps"] = 0
    print("## BP wrong epsilon ##")
    for i in range(G.vcount()):
        err = abs(exact_betw[i] - bp_betw[i])
        if err > args.epsilon * G.vcount() * (G.vcount() - 1) / 2:
            bp_stats["wrong_eps"] += 1
            print("{} {} {} {} {} {} {}".format(i, G.vs[i].degree(),
                 exact_betw[i], bp_betw[i], vc_betw[i], err, err / (G.vcount() * (G.vcount() -1) / 2)))

    # Print statistics to output as CSV
    logging.info("Printing statistics")
    print("graph, nodes, edges, diam, directed, epsilon, delta")
    print("{}, {}, {}, {}, {}, {}, {}".format(G["filename"], G.vcount(),
        G.ecount(), G["diam"], G.is_directed(), args.epsilon, args.delta))
    csvkeys="epsilon, delta, time, sample_size, wrong_eps, err_avg, err_max, err_min, err_stddev, forward_edges_touched, backward_edges_touched, diameter, diam_type"
    print("type", csvkeys)
    print("vc", util.dict_to_csv(vc_stats, csvkeys))
    print("bp", util.dict_to_csv(bp_stats, csvkeys))
    print("exact", util.dict_to_csv(exact_stats, csvkeys))
    
if __name__ == "__main__":
    main()

