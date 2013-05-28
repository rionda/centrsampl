# -*- coding: iso-8859-1 -*-
import argparse
import logging

def number_nodes(string):
    """Read number of nodes from the file path. Return int."""
    logging.info("Reading number of nodes from %s", string)
    #print("path given:",string)
    try:
       with open(string) as file_:
         for line in file_:
           #print(line.find("Nodes: "))
           if line.find("Nodes: ")!= -1:
             index_start = line.find("Nodes: ")
             index_start = index_start + 7
             index_end = line.find(" ",index_start)
             print(line[index_start:index_end])
             return int(line[index_start:index_end])
             
    except OSError as E:
        # XXX There seems to be some problem in the propagation of E.strerror,
        # so the following actually print None at the end. Not our fault. We
        # leave it here as perhaps it will be fixed upstream at some point.
        logging.critical("Cannot read  file %s: %s", path, E.strerror)
        sys.exit(2)
    return 2
    
def main():
   # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path file")
    args = parser.parse_args() 
    number_nodes(args.path)
        
if __name__ == "__main__":
  main()
