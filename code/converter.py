#! /bin/env python3
import argparse
import logging
import os
import os.path
import sys
import igraph as ig

def convert(input_path, is_directed):
    """ Convert a text file to an igraph"""

    G = ig.Graph(directed=is_directed)
    G["rawfile"] = os.path.basename(input_path)
    vertices_num = 0
    edges_num = 0
    try: # Handle OSError
        with open(input_path, 'rt') as input_file:
            logging.info("Conversion started")
            if is_directed:
                logging.debug("Considering graph as directed")
            else:
                logging.debug("Considering graph as undirected")
            for line in input_file:
                # Skip line if it s a comment"
                if line[0] == "#" :
                    logging.debug("Skipping comment line: %s", line)
                    continue
                edge = line.split()
                from_vertex = edge[0]
                to_vertex = edge[1]
                # Add vertices to graph if necessary. When we try to add the
                # first vertex to the graph, a KeyError is raised when try to
                # access G.vs["name"]. Handle it properly and go on.
                try:
                    if not from_vertex in G.vs["name"]:
                        logging.debug("Adding vertex %s", from_vertex)
                        G.add_vertex(name=from_vertex)
                        vertices_num += 1
                except KeyError:                    
                        logging.debug("Adding vertex %s", from_vertex)
                        G.add_vertex(name=from_vertex)
                        vertices_num += 1
                if not to_vertex in G.vs["name"]:
                    logging.debug("Adding vertex %s", to_vertex)
                    G.add_vertex(name=to_vertex)
                    vertices_num += 1

                # Add the edge
                logging.debug("Adding edge %s -> %s", from_vertex, to_vertex)
                G.add_edge(from_vertex, to_vertex)
                edges_num +=1
    except OSError as E:
        logging.critical("Cannot read input file %s: %s", input_path,
                os.strerror(E.errno))
        sys.exit(2)

    logging.info("Conversion complete: %d vertices, %d edges", vertices_num, edges_num)
    return G

def main():
    """ Parse arguments, call convert, write to file."""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "Convert an edge list file to an igraph graph and write it to file in pickle format. The edge list file contains one edge per line as 'from_vertex\tto_vertex'. Lines starting with '#' are treated as comments."
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file (pickle format)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (use multiple times for more verbosity)")
    parser.add_argument("-z", "--compress", action="store_true", default=False, help="compress the output file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--undirected", action="store_true",
            help="consider the graph as undirected (default)", default=True)
    group.add_argument("-d", "--directed", action="store_true", help="consider the graph as directed", default=False)
    args = parser.parse_args()

    # Set the desired level of logging
    log_format='%(levelname)s: %(message)s'
    if args.verbose == 1:
        logging.basicConfig(format=log_format, level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(format=log_format, level=logging.DEBUG)

    # Convert the file
    G = convert(args.input, args.directed)

    # Serialize the graph to file
    logging.info("Writing graph to file %s", args.output)
    if args.compress:
        logging.debug("Compression selected")
        format = "picklez"
    else:
        format = "pickle"
    G.write(args.output, format)

if __name__ == "__main__":
    main()

