#! /usr/bin/env python3
# -*- coding: iso-8859-1 -*-
""" vc_sample_experiment.py
    
    Perform experiment to evaluate the VC sampling algorithm to approximate the
    betweenness centrality of all vertices in a graph. The algorithm is run
    multiple times. We compute aggregate statistics about the runs and save the
    stats and all the results in a single .pickle file.

"""

import argparse
import logging
import math
import os.path
import pickle
import sys

import converter
import util
import vc_sample

def main():
    """Parse arguments, run experiments, collect results and stats, write to file."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "TODO"
    parser.add_argument("epsilon", type=util.valid_interval_float,
            help="accuracy parameter")
    parser.add_argument("delta", type=util.valid_interval_float,
            help="confidence parameter")
    parser.add_argument("runs", type=util.positive_int, default=20, help="number of runs")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("output", help="output file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--approximate", action="store_true",
            default=True, help="use approximate diameter (default)")
    group.add_argument("-d", "--diameter", type=util.positive_int, default=0,
            help="value to use for the diameter")
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="use exact diameter")
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
    parser.add_argument("-v", "--verbose", action="count", default=0,
            help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-w", "--weightFile", default="-",
            help="random weights within the interval 0 to 1, must have as many entries as the number of edges")

    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    if args.pickle:
        G = util.read_graph(args.graph)
    else:
        G = converter.convert(args.graph, not args.undirected, args.maxconn)

    if args.exact:
        args.approximate = False

    # Read the weights    
    weights_list=[]
    if args.weightFile != "-":
        with open(args.weightFile,'r') as weight_file:
            for line in weight_file:
                weights_list.append(float(line.strip()))

    # Perform experiment multiple times
    results = []
    for i in range(args.runs):
        logging.info("Run #%d", i)
        # Compute betweenness
        if args.samplesize:
            results.append(vc_sample.betweenness_sample_size(G,
                args.samplesize, False, args.timeout))
        else:
            if args.diameter > 0:
                results.append(vc_sample.betweenness(G, args.epsilon, args.delta,
                        weights_list, args.diameter, False, args.timeout))
            else:
                results.append(vc_sample.betweenness(G, args.epsilon, args.delta,
                        weights_list, args.approximate, False, args.timeout))

    # Compute aggregate statistics about the experiments
    stats = dict()
    stats["graph"]= os.path.basename(args.graph)
    stats["vertices"] = G.vcount()
    stats["edges"] = G.ecount()
    stats["runs"] = args.runs
    if args.samplesize:
        stats["sample_size"] = args.samplesize
    else:
        stats["delta"] = args.delta
        stats["epsilon"] = args.epsilon
        stats["sample_size"] = results[0][0]["sample_size"]

    stats_names = ["time", "forward_touched_edges", "backward_touched_edges"]
    if not args.samplesize:
        stats_names.append("diameter")
        stats_names.append("diameter_touched_edges")
    for stat_name in stats_names:
        values = sorted([x[0][stat_name] for x in results])
        stats[stat_name + "_max"] = values[-1]
        stats[stat_name + "_min"] = values[0]
        stats[stat_name + "_avg"] = sum(values) / args.runs
        if args.runs > 1:
            stats[stat_name + "_stddev"] = math.sqrt(sum([math.pow(value -
                stats[stat_name + "_avg"], 2) for value in values]) / (args.runs - 1))
        else:
            stats[stat_name + "_stddev"] = 0.0

    stats["betw_min"] = [0.0] * G.vcount()
    stats["betw_max"] = [0.0] * G.vcount()
    stats["betw_avg"] = [0.0] * G.vcount()
    for i in range(G.vcount()):
        betws = sorted([x[1][i] for x in results])
        stats["betw_min"][i]= betws[0]
        stats["betw_max"][i] = betws[-1]
        stats["betw_avg"][i] = sum(betws) / args.runs

    csvkeys="graph, runs, epsilon, delta, sample_size"
    csvkeys_names= ["{0}_avg, {0}_min, {0}_stddev, {0}_max, {0}_min".format(stat_name) 
            for stat_name in stats_names]
    csvkeys_list = [csvkeys] + csvkeys_names
    csvkeys = ",".join(csvkeys_list)
   # print(stats["betw_min"])   
    print(csvkeys)
    print(util.dict_to_csv(stats, csvkeys))
    # Write stats and results to output file
    try: 
        with open(args.output, "wb") as output:
            logging.info("Writing stats and results to %s", args.output)
            pickle.dump((stats, results), output)
            output.close()
            #pkl_file = open("vc_out.picklez", 'rb')
            #reader = pickle.load(pkl_file)
            #print(reader[0]["diameter_touched_edges_avg"])
    except OSError as E:
        logging.critical("Cannot write stats and results to %s: %s",
                args.output, E.strerror)
        sys.exit(2)



if __name__ == "__main__":
    main()

