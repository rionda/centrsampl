#! /usr/bin/env python3
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import logging
import util

import brandes_exact
import brandespich_sample
import vc_sample

def main():
    """Parse arguments, do the comparison, write to output."""
    parser = argparse.ArgumentParser()
    parser.description = "Compare estimation of betweenness centralities to exact values"
    parser.add_argument("epsilon", type=util.valid_interval_float, help="graph file")
    parser.add_argument("delta", type=util.valid_interval_float, help="graph file")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--exact", action="store_true", default=False,
            help="Use exact diameter when computing approx. betweenness using VC-Dimension (default)")
    group.add_argument("-a", "--approximate", action="store_true",
            default=False, help="Use approximate diameter when computing approx. betweenness using VC-Dimension")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    # If the graph does not have the attributes for the betweenness or has the
    # wrong ones, (re-)compute them
    if not "betw_time" in G.attributes():
        brandes_exact.betweenness(G, True)
    if not "vc_betw_time" in G.attributes() or G["vc_eps"] != args.epsilon or G["vc_delta"] != args.delta:
        vc_sample.betweenness(G, args.epsilon, args.delta, args.approximate, True)
    if not "bp_betw_time" in G.attributes() or G["bp_eps"] != args.epsilon or G["bp_delta"] != args.delta:
        brandespich_sample.betweenness(G, args.epsilon, args.delta, True)

    # TODO Compute error statistics
    vc_wrong_eps = 0
    vc_err_max = 0
    vc_err_min = 0
    vc_err_avg = 0
    vc_err_stddev = 0
    bp_wrong_eps = 0
    bp_err_max = 0
    bp_err_min = 0
    bp_err_avg = 0
    bp_err_stddev = 0

    # Print statistics to output as CSV
    print("exact, {}, 0, 0".format(G["betw_time"]))
    print("vc, {}, {}, {}".format(G["vc_betw_time"], vc_wrong_eps, vc_err_max,
        vc_err_min, vc_err_avg, vc_err_stddev))
    print("bp, {}, {}, {}".format(G["bp_betw_time"], bp_wrong_eps, bp_err_max,
        bp_err_min, bp_err_avg, bp_err_stddev))
    
if __name__ == "__main__":
    main()

