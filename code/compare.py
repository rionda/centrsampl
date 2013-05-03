#! /usr/bin/env python3
"""compare.py

Compare estimations of betweenness centralities to exact values. 

"""
import argparse
import logging
import util

def main():
    """Parse arguments, do the comparison, write to output."""
    parser = argparse.ArgumentParser()
    parser.description = "Compare estimation of betweenness centralities to exact values"
    parser.add_argument("epsilon", type=util.valid_interval_float, help="graph file")
    parser.add_argument("delta", type=util.valid_interval_float, help="graph file")
    parser.add_argument("graph", help="graph file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    args = parser.parse_args()

    # Set the desired level of logging
    util.set_verbosity(args.verbose)

    # Read graph
    G = util.read_graph(args.graph)

    if not "betw_time" in G.attributes():
        # TODO compute exact betweenness
        pass
    if not "vc_betw_time" in G.attributes():
        # TODO compute approx betweenness with VC-dim algorithm
        pass
    if not "bp_betw_time" in G.attributes():
        # TODO compute approx betweenness with Brandes and Pich algorithm 
        pass

    # TODO Compute error statistics
    vc_wrong_eps = 0
    vc_err_max = 0
    vc_err_min = 0
    vc_err_avg = 0
    vc_err_stddev = 0
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

