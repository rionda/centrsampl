# -*- coding: iso-8859-1 -*-
import argparse
import logging
import pickle

def get_results(path,field):
    """Read number of nodes from the file path. Return int."""
    logging.info("Reading number of nodes from %s", path)
    pkl_file = open(path, 'rb')
    reader = pickle.load(pkl_file)
    if field not in ["results"] :
        print(reader[0][field])
    else:
        print(reader[1])
    return 2
    
    #print("path given:",string)
    #try:
       #with open(path) as file_:
         #for line in file_:
           #print(line.find("Nodes: "))
           #if line.find("Nodes: ")!= -1:
             #index_start = line.find("Nodes: ")
             #index_start = index_start + 7
             #index_end = line.find(" ",index_start)
             #print(line[index_start:index_end])
             #return int(line[index_start:index_end])
             
    #except OSError as E:
        # XXX There seems to be some problem in the propagation of E.strerror,
        # so the following actually print None at the end. Not our fault. We
        # leave it here as perhaps it will be fixed upstream at some point.
        #logging.critical("Cannot read  file %s: %s", path, E.strerror)
        #sys.exit(2)
    #return 2
    
def main():
   # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path file")
    parser.add_argument("field", help="field of the pickle out file")
    args = parser.parse_args()      
    get_results(args.path,args.field)
        
if __name__ == "__main__":
  main()
