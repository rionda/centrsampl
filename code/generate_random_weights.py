# -*- coding: iso-8859-1 -*-
import argparse
import logging
import pickle
import util
import converter
import random

def generate_random_weights(path,pickle,undirected):
    """Read number of nodes from the file path. Return int."""
    if pickle:
        G = util.read_graph(path)
    else:
        G = converter.convert(path, not undirected, False)

    print(G.ecount())
    txt_dir=path[0:len(path)-4] + "_weights.txt"
    file = open(txt_dir,'w')
    file.write("")

    for line in range(0,G.ecount()):
       file.write(repr(random.random()) + '\n')

    file.close()
    return 0


def main():
   # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path file")
    parser.add_argument("-p", "--pickle", action="store_true", default=False,
            help="use pickle reader for input file")
    parser.add_argument("-u", "--undirected", action="store_true", default=False,
            help="consider the graph as undirected ")
    args = parser.parse_args()
    generate_random_weights(args.path,args.pickle,args.undirected)

if __name__ == "__main__":
  main()
