#! /usr/bin/env python3
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import itertools
import logging
import math
import os.path
import random

import brandes_exact
import brandespich_sample
import converter
import diameter
import geisbergerss_sample
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
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0,
            help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter when computing approximation of betweenness using VC-Dimension")
    parser.add_argument("-m", "--maxconn", action="store_true", default=False,
            help="if the graph is not weakly connected, only save the largest connected component")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-r", "--resultfiles", nargs=4, 
    help="Use results files rather than recomputing betweenness. Files should be specified as 'exact_res vc_res bp_res gss_res'")
    parser.add_argument("-s", "--samplesize", type=util.positive_int,
            default=0, help="use specified sample size. Overrides epsilon, delta, and diameter computation")
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

    # Seed the random number generator
    random.seed()

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    if args.exact:
        args.approximate = False

    if not args.resultfiles:
        (exact_stats, exact_betw) = brandes_exact.betweenness(G, args.write,
                args.timeout)
        if args.samplesize: 
            (vc_stats, vc_betw) = vc_sample.betweenness_sample_size(G,
                    args.samplesize, args.write, args.timeout)
            (bp_stats, bp_betw) = brandespich_sample.betweenness_sample_size(G,
                    args.samplesize, args.write, args.timeout)
            (gss_stats, gss_betw) = geisbergerss.betweenness_sample_size(G,
                    args.samplesize, args.write, args.timeout)
        else:
            if args.diameter > 0:
                (vc_stats, vc_betw) = vc_sample.betweenness(G, args.epsilon, args.delta,
                        args.diameter, args.write, args.timeout)
            else:
                (vc_stats, vc_betw) = vc_sample.betweenness(G, args.epsilon, args.delta,
                        args.approximate, args.write, args.timeout)

            (bp_stats, bp_betw) = brandespich_sample.betweenness(G,
                    args.epsilon, args.delta, args.write, args.timeout)
            (gss_stats, gss_betw) = geisbergerss_sample.betweenness(G,
                    args.epsilon, args.delta, args.write, args.timeout)
    else:
        (exact_stats, exact_betw) = util.read_stats_betw(args.result_files[0])
        (vc_stats, vc_betw) = util.read_stats_betw(args.result_files[1])
        (bp_stats, bp_betw) = util.read_stats_betw(args.result_files[2])
        (gss_stats, gss_betw) = util.read_stats_betw(args.result_files[3])

    #Compute useful graph statistics (mainly diameter)
    if "diam" not in G.attributes():
        diameter.diameter(G)

    # If specified, write betweenness as vertex attributes, and time and
    # diameter as graph attributes back to file

    if args.write:
        logging.info("Writing betweenness as vertex attributes and stats as graph attribute")
        if args.write == "auto":
            filename = os.path.splitext(args.graph)[0] + ("-undir" if args.undirected else "dir") + ".picklez"
            G.write(filename)
        else:
            G.write(args.write)

    # Compute error statistics
    # It is not a problem to sort the error by value because we only compute
    # aggregates.
    logging.info("Computing error statistics")
    max_err = args.epsilon * G.vcount() * (G.vcount() - 1) / 2
    vc_errs = sorted([abs(a - b) for a,b in zip(exact_betw,vc_betw)])
    vc_stats["err_avg"] = sum(vc_errs) / G.vcount()
    vc_stats["err_max"] = vc_errs[-1]
    vc_stats["err_min"] = list(itertools.filterfalse(lambda x: x == 0, vc_errs))[0]
    vc_stats["err_stddev"] = math.sqrt(sum([math.pow(err - vc_stats["err_avg"], 2) for err in vc_errs]) / (G.vcount() -1))
    #vc_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
    #    G.vcount() * (G.vcount() - 1) / 2, vc_errs)))
    vc_stats["wrong_eps"] = 0;
    for i in range(10):
        vc_stats["err_decile_" + str(i)] = 0;
    for i in range(G.vcount()):
        err = abs(exact_betw[i] - vc_betw[i])
        vc_stats["err_decile_" + util.decile(err, max_err)] += 1
        if err > max_err:
            vc_stats["wrong_eps"] += 1
            if vc_stats["wrong_eps"] == 1:
                print("## VC wrong epsilon ##")
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
    for i in range(10):
        bp_stats["err_decile_" + str(i)] = 0;
    for i in range(G.vcount()):
        err = abs(exact_betw[i] - bp_betw[i])
        bp_stats["err_decile_" + util.decile(err, max_err)] += 1
        if err > max_err:
            bp_stats["wrong_eps"] += 1
            if bp_stats["wrong_eps"] == 1:
                print("## BP wrong epsilon ##")
            print("{} {} {} {} {} {} {}".format(i, G.vs[i].degree(),
                 exact_betw[i], bp_betw[i], vc_betw[i], err, err / (G.vcount() * (G.vcount() -1) / 2)))

    gss_errs = sorted([abs(a - b) for a,b in zip(exact_betw,gss_betw)])
    gss_stats["err_avg"] = sum(gss_errs) / G.vcount()
    gss_stats["err_max"] = max(gss_errs)
    gss_stats["err_min"] = list(itertools.filterfalse(lambda x: x == 0, gss_errs))[0]
    gss_stats["err_stddev"] = math.sqrt(sum([math.pow(err - gss_stats["err_avg"], 2) for err in gss_errs]) / (G.vcount() -1))
    #gss_wrong_eps = len(list(itertools.filterfalse(lambda x: x <= args.epsilon *
    #    G.vcount() * (G.vcount() - 1) / 2, gss_errs)))
    gss_stats["wrong_eps"] = 0
    for i in range(10):
        gss_stats["err_decile_" + str(i)] = 0;
    for i in range(G.vcount()):
        err = abs(exact_betw[i] - gss_betw[i])
        gss_stats["err_decile_" + util.decile(err, max_err)] += 1
        if err > max_err:
            gss_stats["wrong_eps"] += 1
            if gss_stats["wrong_eps"] == 1:
                print("## BP wrong epsilon ##")
            print("{} {} {} {} {} {} {}".format(i, G.vs[i].degree(),
                 exact_betw[i], gss_betw[i], vc_betw[i], err, err / (G.vcount() * (G.vcount() -1) / 2)))

    # Print statistics to output as CSV
    logging.info("Printing statistics")
    print("graph, nodes, edges, diam, directed, epsilon, delta, sample_size")
    print("{}, {}, {}, {}, {}, {}, {}, {}".format(G["filename"], G.vcount(),
        G.ecount(), G["diam"], G.is_directed(), args.epsilon, args.delta,
        args.samplesize))
    csvkeys="epsilon, delta, sample_size, time, wrong_eps, err_avg, err_max, err_min, err_stddev, forward_touched_edges, backward_touched_edges, diameter_touched_edges, err_decile_0, err_decile_1, err_decile_2, err_decile_3, err_decile_4, err_decile_5, err_decile_6, err_decile_7, err_decile_8, err_decile_9, diameter, diam_type"
    print("type,", csvkeys)
    print("vc,", util.dict_to_csv(vc_stats, csvkeys))
    print("bp,", util.dict_to_csv(bp_stats, csvkeys))
    print("gss,", util.dict_to_csv(gss_stats, csvkeys))
    print("exact,", util.dict_to_csv(exact_stats, csvkeys))
    
if __name__ == "__main__":
    main()

