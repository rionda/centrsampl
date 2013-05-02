#! /bin/env python3

import argparse
import logging
import math
import igraph as ig

def sample_size(epsilon, delta, vcdim_upper_bound, c=0.5):
    """ Compute the sample size to achieve an epsilon-approximation of a range
    set with VC-dimension at most vcdim_upper_bound with probability at least 1-delta
    """
    return (c / math.pow(epsilon, 2)) * ( vcdim_upper_bound + math.log(1 / delta) )

def main():
    """Compute approximations of the betweenness centrality of all the vertices  
    in the graph using random sampling and the VC-dimension
    """
    # TODO Implement everything.
    pass

if __name__ == "__main__":
    main()

