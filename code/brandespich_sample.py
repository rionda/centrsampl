#! /bin/env python3

import argparse
import logging
import math
import igraph as ig

def get_sample_size(epsilon, delta, vertices_num):
    """ Compute the sample size to achieve an epsilon-approximation of for the
    betweenness centralities of the vertices of a graph with vertices_num
    vertices, with probability at least 1-delta
    """
    return int(math.ceil((2 * math.pow((vertices_num - 2) / (epsilon *
        (vertices_num -1)), 2) * math.log(2 * vertices_num / delta))))

def main():
    """Compute approximations of the betweenness centrality of all the vertices
    in the graph using the algorithm by Brandes and Pich
    http://www.worldscientific.com/doi/abs/10.1142/S0218127407018403  
    """
    # TODO Implement everything.
    pass

if __name__ == "__main__":
    main()


